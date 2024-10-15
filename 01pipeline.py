from transformers import pipeline
sentiment_analysis = pipeline("sentiment-analysis")

# 감정 분석 예제
sentence = '''
I have never before faced Dymphna in tournament play, nor played with 
the sonic balls the blind require, but I watched him barely dispatch Petropolis Kahn in 
the Round of 16, and I know he is mine. It will start in the E.R., at the intake desk if C.T.'s 
late in following the ambulance, or in the green-tiled room after the room with the 
invasive-digital machines; or, given this special M.D.-supplied ambulance, maybe on the 
ride itself: some blue-jawed M.D. scrubbed to an antiseptic glow with his name sewn in 
cursive on his white coat's breast pocket and a quality desk-set pen, wanting gurneyside 
Q&A, etiology and diagnosis by Socratic method, ordered and point-by-point. There are, 
by the O.E.D. VI's count, nineteen nonarchaic synonyms for unresponsive, of which nine 
are Latinate and four Saxonic. I will play either Stice or Polep in Sunday's final. Maybe in 
front of Venus Williams. It will be someone blue-collar and unlicensed, though, 
inevitably — a nurse's aide with quick-bit nails, a hospital security guy, a tired Cuban 
orderly who addresses me as jou — who will, looking down in the middle of some kind 
of bustled task, catch what he sees as my eye and ask So yo then man what's your story? '''
results= sentiment_analysis(sentence)
print(results)
  # [{'label': 'POSITIVE', 'score': 0.99}]
