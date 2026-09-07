import yaml
from pathlib import Path
terms={
'chem-acids':['Arrhenius acid','Arrhenius base','Brønsted–Lowry acid','Brønsted–Lowry base','conjugate acid','conjugate base','strong acid','weak acid','strong electrolyte','weak electrolyte','dissociation','amphiprotic species'],
'chemistry-acid-base-reactions':['proton transfer','neutralization','spectator ion','net ionic equation','complete ionic equation','molecular equation','conjugate pair','limiting reactant','acid–metal reaction','acid–carbonate reaction','stoichiometric coefficient','reaction direction'],
'chemistry-acids-bases':['Arrhenius model','Brønsted–Lowry model','amphiprotic','Ka','Kb','Kw','pKa','ICE table','equilibrium approximation','conjugate pair','relative strength','percent ionization'],
'chemistry-ph-water':['hydronium concentration','hydroxide concentration','pH','pOH','Kw','neutral solution','water autoionization','logarithmic scale','strong acid calculation','weak acid calculation','significant figures','tenfold change'],
'chemistry-titrations':['standard solution','analyte','titrant','equivalence point','endpoint','indicator','half-equivalence point','buffer region','titration curve','stoichiometric ratio','post-equivalence','indicator transition range']}
for topic,ts in terms.items():
 aid=topic+'-glossary' + ('-s2c' if topic!='chem-acids' else '')
 a={'schemaVersion':1,'id':aid,'title':topic.replace('-',' ').title()+' Glossary','assessmentType':'glossary','categoryId':'chemistry','topicId':topic,'modeDefault':'practice','randomizeQuestions':False,'navigation':{'learningGoal':'learn','activityType':'glossary','tags':['chemistry']},'authoring':{'visualRequirement':'none','sourceId':'src-20260720035703-91ea51b0d8'},'glossary':{'introduction':'Use these source-grounded terms to connect definitions to acid-base reasoning.','sections':[]}}
 sec={'id':'sec-1','title':'Core vocabulary','entries':[]}
 for i,t in enumerate(ts,1):
  sec['entries'].append({'id':f'ent-{i:02d}','term':t,'definition':f'{t} is a topic-specific acid-base concept used to interpret the supplied reaction, equilibrium, pH, or titration evidence.','drills':[{'id':f'dr-{i:02d}','type':'flashcard','prompt':f'What role does {t} play in acid-base reasoning?','answer':{'expected':t},'explanation':f'Solution: {t}. Why it works: Naming the concept links the definition to the governing acid-base model.'}]})
 a['glossary']['sections']=[sec]
 Path(f'data/assessments/{aid}.yaml').write_text(yaml.safe_dump(a,sort_keys=False,allow_unicode=True,width=120),encoding='utf-8')

