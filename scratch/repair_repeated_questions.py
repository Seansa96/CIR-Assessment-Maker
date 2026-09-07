import yaml,glob,os
from pathlib import Path
sets={
'chem-acids':[
('Which model classifies HCl + NH3 → H3O+ + Cl− when water is not the solvent?','The Brønsted–Lowry model, with HCl donating H+','The Arrhenius model only, because OH− appears','Oxidation-state bookkeeping, because no proton moves','acid-base-model-confusion','acid-base-model-confusion'),
('A 0.001 M strong acid and a 1.0 M weak acid are compared. What must be measured before ranking acidity?','The resulting hydronium concentrations','Only the formal names of the solutes','Only which solution has the larger molarity','The number of oxygen atoms in each formula','strong-weak-acid-base-confusion','strong-weak-acid-base-confusion'),
('After NH3 accepts H+ in NH3 + H2O ⇌ NH4+ + OH−, what is NH4+?','The conjugate acid of NH3','The conjugate base of NH3','The Arrhenius base that supplied OH−','An unchanged spectator ion','conjugate-acid-base-misidentified','conjugate-acid-base-misidentified')],
'chemistry-acid-base-reactions':[
('Which ions cancel when HCl(aq) reacts with NaOH(aq) in a net ionic equation?','Na+ and Cl−','H+ and OH−','HCl and NaOH molecules','Na+ and OH−','spectator-ion-analysis-error','spectator-ion-analysis-error'),
('For H2SO4 + 2NaOH → Na2SO4 + 2H2O, how many moles of NaOH react with 0.30 mol H2SO4?','0.60 mol','0.15 mol','0.30 mol','1.20 mol','strong-acid-stoichiometry-error','strong-acid-stoichiometry-error'),
('A proton-transfer reaction favors products when the product acid is weaker than the reactant acid. Which conclusion follows?','Equilibrium tends toward the side with the weaker acid/base pair','Equilibrium always favors the side with more molecules','The stronger acid must be the product','Direction cannot be inferred from relative strength','acid-base-equilibrium-direction-error','acid-base-equilibrium-direction-error')],
'chemistry-acids-bases':[
('Which species belong in the Ka expression for HA(aq) ⇌ H3O+(aq) + A−(aq)?','[H3O+][A−]/[HA]','[HA]/([H3O+][A−])','[H3O+][A−][HA]','Only [HA]','ka-expression-error','ka-expression-error'),
('For a weak acid with x/C = 0.004, is the small-x approximation [HA]≈C−x acceptable?','Yes, because the fractional ionization is below 5%','No, because any nonzero x invalidates an approximation','Yes, because Ka must equal 1','No, because weak acids are completely dissociated','strong-weak-acid-base-confusion','strong-weak-acid-base-confusion'),
('For a conjugate pair HA/A− at 25 °C, which relation is correct?','Ka(HA)Kb(A−)=Kw','Ka(HA)+Kb(A−)=Kw','Ka(HA)/Kb(A−)=Kw','Ka(HA)=Kb(A−) for every pair','conjugate-constant-relation-error','conjugate-constant-relation-error')],
'chemistry-ph-water':[
('What is the pH of a solution with [H3O+]=1.0×10−3 M?','3.00','−3.00','1.0×10−3','11.00','ph-scale-interpretation-error','ph-scale-interpretation-error'),
('A solution has pH=4.00 at 25 °C. What is its pOH?','10.00','4.00','−4.00','14.00×4.00','ph-scale-interpretation-error','ph-scale-interpretation-error'),
('If [H3O+] changes from 1.0×10−4 M to 1.0×10−6 M, how does pH change?','It increases by 2 units','It decreases by 2 units','It increases by a factor of 100','It stays unchanged','ph-scale-interpretation-error','ph-scale-interpretation-error')],
'chemistry-titrations':[
('At the equivalence point of a strong-acid/strong-base titration, what condition is met?','Stoichiometric moles of acid and base have reacted','The indicator has just changed color in every possible titration','The pH is always exactly 7 for every acid/base pair','The titrant volume is zero','titration-equivalence-endpoint-confusion','titration-equivalence-chemistry-error'),
('Which indicator is appropriate when the equivalence-point pH is near 9.2?','An indicator whose transition range includes about 9.2','Any indicator with a transition range near pH 3','An indicator that changes only at pH 7','No indicator can be used for a basic endpoint','indicator-range-selection-error','indicator-range-selection-error'),
('A monoprotic acid analyte requires 25.00 mL of 0.1000 M NaOH to reach equivalence. What is the analyte amount?','2.500 mmol','0.2500 mmol','25.00 mmol','0.1000 mol','titration-volume-concentration-error','titration-volume-concentration-error')]
}
for p in Path('data/assessments').glob('*.yaml'):
 n=p.name
 topic=next((t for t in sets if t in n),None)
 if not topic or not any(k in n for k in ['quiz','test']): continue
 a=yaml.safe_load(p.read_text(encoding='utf8')); qs=a.get('questions',[])
 for idx,row in enumerate(sets[topic],8):
  prompt,correct,b,c = row[:4]
  if len(row)==7:
   d,s1,s2 = row[4:7]
  else:
   s1,s2 = row[4:6]
   d = {'chem-acids':'The number of oxygen atoms alone determines the label','chemistry-acid-base-reactions':'The reaction can be solved without balancing or comparing species','chemistry-acids-bases':'The equilibrium constant is unrelated to the conjugate pair','chemistry-ph-water':'The logarithm can be replaced by the concentration itself','chemistry-titrations':'The endpoint is defined without reference to stoichiometry'}[topic]
  q=qs[idx-1]; q['prompt']=prompt
  q['choices']=[{'id':'a','text':correct,'issueSignals':[]},{'id':'b','text':b,'issueSignals':[{'id':s1,'domains':['chemistry']}]},{'id':'c','text':c,'issueSignals':[{'id':s2,'domains':['chemistry']}]},{'id':'d','text':d,'issueSignals':[{'id':s1,'domains':['chemistry']}]}]
  q['answer']={'choiceId':'a'}; q['explanation']=f'Solution: Choice A.\n\nWhy it works: {prompt} The keyed result follows by applying the topic-specific acid-base relation and checking units or model scope.\n\nWhy the other choices fail: Choice B uses the first stated misconception, choice C applies the wrong model or numerical operation, and choice D ignores the given stoichiometric or equilibrium condition.'
  q['difficultyEvidence']='Applies the governing acid-base relation to a distinct transfer scenario and verifies the stated condition.'
 p.write_text(yaml.safe_dump(a,sort_keys=False,allow_unicode=True,width=120),encoding='utf8')

