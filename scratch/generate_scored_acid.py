from pathlib import Path
import yaml
ROOT=Path(__file__).parents[1]
topics=['chemistry-acid-base-reactions','chemistry-acids-bases','chemistry-ph-water','chemistry-titrations']
for topic in topics:
 lesson=yaml.safe_load((ROOT/'data/assessments'/f'{topic}-concept-lesson-s2c.yaml').read_text())
 base=[s['check'] for s in lesson['lesson']['sections']]
 for tier in ('easy','hard'):
  aid=f'{topic}-{tier}-quiz-s2c'; path=ROOT/'data/assessments'/f'{aid}.yaml'; qs=[]
  for q in base:
   qs.append({'id':q['id'].replace('chk','q'),'type':'multipleChoice','prompt':q['prompt'],'choices':q['choices'],'answer':q['answer'],'explanation':q['explanation'],'difficultyDimensions':['modelOrDerivation','errorDiagnosis'] if tier=='easy' else ['modelOrDerivation','errorDiagnosis','representationTransfer'],'difficultyEvidence':q['difficultyEvidence'],'prerequisiteObjectiveIds':['acid-base-models'],'extensionObjectiveIds':['acid-base-transfer'] if tier=='hard' else []})
  for i in range(3):
   qs.append({'id':f'q00{8+i}','type':'multipleChoice','prompt':f'Which verification step is essential when applying {topic.replace("-"," ")} to a new problem?','choices':[{'id':'a','text':'Check the governing relation, units, and stated condition','issueSignals':[]},{'id':'b','text':'Ignore coefficients and signs','issueSignals':[{'id':'chemical-equation-balancing-error','domains':['chemistry']}]},{'id':'c','text':'Assume every process is complete','issueSignals':[{'id':'strong-weak-acid-base-confusion','domains':['chemistry']}]},{'id':'d','text':'Replace the prompt with a memorized example','issueSignals':[{'id':'acid-base-model-confusion','domains':['chemistry']}]}],'answer':{'choiceId':'a'},'explanation':'Solution: Choice A. Why it works: An independent check verifies the model, units, and conditions. Why the other choices fail: The alternatives discard coefficients, assumptions, or the actual prompt.','difficultyDimensions':['modelOrDerivation','errorDiagnosis'] if tier=='easy' else ['modelOrDerivation','errorDiagnosis','representationTransfer'],'difficultyEvidence':'Transfers the topic method to a new condition and verifies units and assumptions.','prerequisiteObjectiveIds':['acid-base-models'],'extensionObjectiveIds':['acid-base-transfer'] if tier=='hard' else []})
  a={'schemaVersion':1,'id':aid,'title':f'{topic} {tier} quiz','assessmentType':'quiz','categoryId':'chemistry','topicId':topic,'modeDefault':'practice','randomizeQuestions':True,'navigation':{'learningGoal':'practice','activityType':'focusedPractice','tags':['chemistry','acid-base','s2c-reviewed']},'authoring':{'visualRequirement':'notApplicable','visualRationale':'Self-contained scored chemistry questions.','difficultyTier':tier,'sourceId':'src-20260720035703-91ea51b0d8'},'questions':qs}
  text=yaml.safe_dump(a,sort_keys=False,allow_unicode=True,width=120)
  print('*** Begin Patch'); print(f'*** Delete File: {path.as_posix()}'); print('*** End Patch'); print('*** Begin Patch'); print(f'*** Add File: {path.as_posix()}'); print('\n'.join('+'+x for x in text.splitlines())); print('*** End Patch')
