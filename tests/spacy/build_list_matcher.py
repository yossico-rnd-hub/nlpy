#!env/bin/python

# Load required modules
from spacy.matcher import Matcher
from spacy.attrs import IS_PUNCT, LOWER
import spacy

nlp = spacy.load('en')
matcher = Matcher(nlp.vocab)

def skillPattern(skill):
    pattern = []
    for b in skill.split():
        pattern.append({'LOWER':b})  
    return pattern

def buildPatterns(skills):
    pattern = []
    for skill in skills:
        pattern.append(skillPattern(skill))
    return list(zip(skills, pattern))

def on_match(matcher, doc, id, matches):
    return matches

def buildMatcher(patterns):
    for pattern in patterns:
        matcher.add(pattern[0], on_match, pattern[1])
    return matcher

cities = [ 
    u'delhi',
    u'bengaluru',
    u'kanpur',
    u'noida',
    u'ghaziabad',
    u'chennai',
    u'hydrabad',
    u'luckhnow',
    u'saharanpur',
    u'dehradun',
    u'bombay'
]

patterns = buildPatterns(cities)
city_matcher = buildMatcher(patterns)

def cityMatcher(matcher, text):
    skills = []
    doc = nlp(unicode(text.lower()))
    matches = matcher(doc)
    for b in matches:
        match_id, start, end = b
        print(doc[start : end])

cityMatcher(city_matcher, "I am from Saharanpur, i live in bengaluru..")
