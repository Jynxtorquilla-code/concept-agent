"""
Natuurhuisje Agent V2 - Improved with Few-Shot Learning
Gebruikt jouw gelabelde voorbeelden voor betere resultaten
"""

import json
import re
import csv
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from anthropic import Anthropic
import os

@dataclass
class LabeledExample:
    """Een gelabeld voorbeeld natuurhuisje"""
    url: str
    category: str
    score: float
    reasoning: str
    key_features: List[str]

@dataclass
class ScoringResult:
    is_natuurhuisje: bool
    confidence_score: float
    category: str
    reasoning: str
    breakdown: Dict[str, float]
    similar_to: Optional[str] = None  # Welk voorbeeld lijkt het meest op

class ImprovedNatuurhuisjeAgent:
    """
    Verbeterde agent met few-shot learning
    """
    
    def __init__(self, api_key: str = None, training_file: str = 'training_data.csv'):
        """Initialize with optional training data"""
        self.client = Anthropic(api_key=api_key) if api_key else Anthropic()
        
        # Criteria (same as before)
        self.criteria = {
            "natuur_nabijheid": {
                "weight": 30,
                "description": "Afstand tot en integratie met natuur"
            },
            "privacy_rust": {
                "weight": 20,
                "description": "Mate van privacy en rust (vrijstaand, kleinschalig)"
            },
            "omgeving_kwaliteit": {
                "weight": 25,
                "description": "Kwaliteit natuuromgeving (bos, strand, heide, bergen)"
            },
            "authenticiteit": {
                "weight": 15,
                "description": "Natuurhuisje gevoel vs. standaard vakantiepark"
            },
            "bebouwing": {
                "weight": 10,
                "description": "Afwezigheid van stedelijke bebouwing/massa toerisme"
            }
        }
        
        # Load training data if available
        self.training_examples = self._load_training_data(training_file)
        print(f"✅ Geladen: {self._count_examples()} training voorbeelden")
    
    def _load_training_data(self, filename: str) -> Dict[str, List[LabeledExample]]:
        """Load training examples from CSV"""
        examples = {"ja": [], "nee": []}
        
        if not os.path.exists(filename):
            print(f"⚠️  Geen training data gevonden ({filename})")
            print("   Run eerst: python training_data_tool.py")
            return examples
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Skip template rows
                    if 'XXXXX' in row['URL'] or 'YYYYY' in row['URL']:
                        continue
                    
                    example = LabeledExample(
                        url=row['URL'],
                        category=row['Categorie'],
                        score=float(row['Score']) if row['Score'] else 50.0,
                        reasoning=row['Redenering'],
                        key_features=row['Kenmerken'].split('; ') if row['Kenmerken'] else []
                    )
                    
                    if example.category in examples:
                        examples[example.category].append(example)
        except Exception as e:
            print(f"⚠️  Kon training data niet laden: {e}")
        
        return examples
    
    def _count_examples(self) -> str:
        """Count training examples"""
        counts = {cat: len(exs) for cat, exs in self.training_examples.items()}
        total = sum(counts.values())
        return f"{total} total (JA: {counts['ja']}, TWIJFEL: {counts['twijfel_nee']}, NEE: {counts['nee']})"
    
    def _build_few_shot_prompt(self, listing_data: Dict) -> str:
        """Build improved prompt with few-shot examples"""
        
        prompt = """Analyseer deze vakantieaccommodatie en bepaal of het een echt "natuurhuisje" is.

"""
        
        # Add examples if we have them
        if any(len(exs) > 0 for exs in self.training_examples.values()):
            prompt += """Ik heb al enkele voorbeelden gelabeld. Gebruik deze als referentie:

"""
            
            # Add JA examples
            ja_examples = self.training_examples.get('ja', [])[:2]  # Max 2
            if ja_examples:
                prompt += "═══ JA - NATUURHUISJE (60-100 punten) ═══\n\n"
                for ex in ja_examples:
                    prompt += f"""✓ Voorbeeld (Score: {ex.score}/100):
   Redenering: {ex.reasoning}
   Kenmerken: {', '.join(ex.key_features[:3])}

"""
            
            # Add NEE examples
            nee_examples = self.training_examples.get('nee', [])[:2]
            if nee_examples:
                prompt += "═══ NEE - GEEN NATUURHUISJE (0-59 punten) ═══\n\n"
                for ex in nee_examples:
                    prompt += f"""✗ Voorbeeld (Score: {ex.score}/100):
   Redenering: {ex.reasoning}
   Kenmerken: {', '.join(ex.key_features[:3])}

"""
            
            prompt += "═══════════════════════════════════════════════\n\n"
        
        # Add base criteria
        prompt += f"""
CRITERIA (gebruik de voorbeelden als kalibratie):

1. natuur_nabijheid (30% gewicht): Hoe dichtbij en toegankelijk is de natuur?
2. privacy_rust (20% gewicht): Hoeveel privacy en rust biedt de locatie?
3. omgeving_kwaliteit (25% gewicht): Hoe mooi/bijzonder is de natuuromgeving?
4. authenticiteit (15% gewicht): Voelt het als authentiek natuurhuisje?
5. bebouwing (10% gewicht): Hoe afwezig is stedelijke bebouwing?

TE ANALYSEREN HUISJE:
Type: {listing_data.get('type', 'Onbekend')}
Beschrijving: {listing_data.get('description', 'Niet beschikbaar')[:500]}
Omgeving: {listing_data.get('location_info', 'Niet beschikbaar')[:500]}

Geef voor elk criterium een score van 0-10, en vermeld welk voorbeeld (JA/TWIJFEL/NEE) het meest lijkt.

Antwoord in dit exacte JSON formaat:
{{
    "natuur_nabijheid": <score 0-10>,
    "privacy_rust": <score 0-10>,
    "omgeving_kwaliteit": <score 0-10>,
    "authenticiteit": <score 0-10>,
    "bebouwing": <score 0-10>,
    "reasoning": "<gedetailleerde uitleg, refereer naar voorbeelden als relevant>",
    "similar_to": "<'ja' of 'nee' - welke categorie lijkt het meest op>",
    "key_observations": ["<observatie 1>", "<observatie 2>", "<observatie 3>"]
}}
"""
        
        return prompt
    
    def analyze_listing(self, url: str, html_content: str) -> ScoringResult:
        """Main analysis function with few-shot learning"""
        
        # Extract listing data
        listing_data = self._extract_listing_data(html_content)
        
        # Build improved prompt
        prompt = self._build_few_shot_prompt(listing_data)
        
        # Call Claude
        message = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        # Parse response
        response_text = message.content[0].text
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        
        if json_match:
            analysis = json.loads(json_match.group())
        else:
            # Fallback
            analysis = {
                "natuur_nabijheid": 5,
                "privacy_rust": 5,
                "omgeving_kwaliteit": 5,
                "authenticiteit": 5,
                "bebouwing": 5,
                "reasoning": "Kon analyse niet voltooien",
                "similar_to": "nee",
                "key_observations": []
            }
        
        # Calculate score
        result = self._calculate_final_score(analysis)
        
        return result
    
    def _extract_listing_data(self, html_content: str) -> Dict:
        """Extract relevant data from HTML (same as before)"""
        data = {
            "description": "",
            "location_info": "",
            "type": "",
            "facilities": []
        }
        
        # Extract description
        desc_pattern = r'<h2>.*?</h2>\s*<p>(.*?)</p>'
        matches = re.findall(desc_pattern, html_content, re.DOTALL)
        if matches:
            data["description"] = " ".join(matches)
        
        # Extract location
        if "Natuur en omgeving" in html_content:
            env_section = html_content.split("Natuur en omgeving")[1].split("</div>")[0]
            data["location_info"] = re.sub(r'<[^>]+>', '', env_section)[:1000]
        
        # Extract type
        type_patterns = [
            r'(Kleinschalig vakantiepark)',
            r'(Vrijstaand)',
            r'(Chalet)',
            r'(Blokhut)',
            r'(Boomhut)',
        ]
        for pattern in type_patterns:
            if re.search(pattern, html_content):
                data["type"] = re.search(pattern, html_content).group(1)
                break
        
        return data
    
    def _calculate_final_score(self, analysis: Dict) -> ScoringResult:
        """Calculate final score (same as before, but with similar_to)"""
        
        total_score = 0
        breakdown = {}
        
        for criterion, config in self.criteria.items():
            score = analysis.get(criterion, 5)
            weighted = (score / 10) * config["weight"]
            total_score += weighted
            breakdown[criterion] = score
        
        # Binary classification: only JA or NEE
        if total_score >= 60:  # Threshold for JA
            category = "✅ Natuurhuisje"
            is_natuurhuisje = True
        else:
            category = "❌ Geen natuurhuisje"
            is_natuurhuisje = False
        
        return ScoringResult(
            is_natuurhuisje=is_natuurhuisje,
            confidence_score=total_score,
            category=category,
            reasoning=analysis.get("reasoning", ""),
            breakdown=breakdown,
            similar_to=analysis.get("similar_to", "unknown")
        )
    
    def format_result(self, result: ScoringResult) -> str:
        """Format result for display"""
        
        output = f"""
{'='*60}
NATUURHUISJE ANALYSE (V2 - Met Training Data)
{'='*60}

OORDEEL: {result.category}
SCORE: {result.confidence_score:.1f}/100
"""
        
        if result.similar_to:
            similarity_label = {
                'ja': '✓ Lijkt op JA voorbeelden',
                'twijfel_nee': '◐ Lijkt op TWIJFEL voorbeelden',
                'nee': '✗ Lijkt op NEE voorbeelden'
            }
            output += f"VERGELIJKBAAR MET: {similarity_label.get(result.similar_to, result.similar_to)}\n"
        
        output += "\nCRITERIUM BREAKDOWN:\n"
        
        for criterion, score in result.breakdown.items():
            config = self.criteria[criterion]
            bar = "█" * int(score) + "░" * (10 - int(score))
            output += f"\n{config['description']:<45} {bar} {score:.1f}/10"
        
        output += f"""

REDENERING:
{result.reasoning}

{'='*60}
"""
        return output


# Convenience function
def analyze_with_training(url: str, html_content: str, training_file: str = 'training_data.csv'):
    """Quick function to analyze with training data"""
    agent = ImprovedNatuurhuisjeAgent(training_file=training_file)
    return agent.analyze_listing(url, html_content)


if __name__ == "__main__":
    print("""
╔════════════════════════════════════════════════════════════╗
║  Natuurhuisje Agent V2 - Improved with Training Data      ║
╚════════════════════════════════════════════════════════════╝

Deze versie gebruikt jouw gelabelde voorbeelden voor betere resultaten!

USAGE:
    from natuurhuisje_agent_v2 import ImprovedNatuurhuisjeAgent
    
    agent = ImprovedNatuurhuisjeAgent(training_file='training_data.csv')
    result = agent.analyze_listing(url, html)
    print(agent.format_result(result))

Zorg dat training_data.csv bestaat en gevuld is!
""")
