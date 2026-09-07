from pathlib import Path
import yaml, json, difflib
ROOT=Path(__file__).parents[1]
base=yaml.safe_load((ROOT/'data/assessments/physics2-ch05-continuous-charge-concept-lesson.yaml').read_text())
SID='src-20260806094518-3f5d8d0e38'

configs={
'coulombs-law': {
 'aid':'physics2-ch05-coulombs-law-concept-lesson','title':"Coulomb's Law & Superposition",'bp':'physics2-coulombs-superposition-calculus-v1','packet':'packet-physics2-coulombs-superposition-calculus-v1',
 'skills':['coulombs-law','vector-superposition','inverse-square-law','unit-analysis','evaluate-limits'],
 'sections':[
 ('Point-charge interaction','Start with two signed point charges. The force on $q_2$ due to $q_1$ has magnitude $F=k|q_1q_2|/r^2$ and points along the line joining them. A positive product means repulsion; a negative product means attraction. The scalar magnitude is never a substitute for deciding direction.','Two charges $q_1=+2\,\mu\mathrm C$ and $q_2=-3\,\mu\mathrm C$ are separated by $r$. Which direction is the force on $q_2$?',['away from $q_1$','toward $q_1$','perpendicular to the line','zero'],'b'),
 ('Signed vectors, not signed magnitudes','Write the vector law as $\mathbf F_{12}=kq_1q_2(\mathbf r_2-\mathbf r_1)/|\mathbf r_2-\mathbf r_1|^3$. The signed product controls attraction or repulsion while the displacement supplies direction. Keep source and target labels explicit before substituting.','With $q_1<0$, $q_2>0$, and $\mathbf r_2-\mathbf r_1=3\hat{\mathbf x}$, what is the direction of $\mathbf F_{12}$?',['$+\hat{\mathbf x}$','$-\hat{\mathbf x}$','$+\hat{\mathbf y}$','direction cannot be determined'],'b'),
 ('Inverse-square scaling','Holding charges fixed, doubling separation changes force by $(1/2)^2$, so $F$ becomes one-fourth. This is a geometric dilution law, not a linear proportionality. Check the exponent before calculating.','If $r$ changes from $r$ to $3r$ with charges unchanged, how does $|F|$ change?',['It triples','It becomes one-third','It becomes one-ninth','It becomes nine times larger'],'c'),
 ('Superposition of several charges','For several source charges, calculate each vector force at the same target and add components: $\mathbf F=\sum_i\mathbf F_i$. Do not add magnitudes unless all forces are collinear and same direction.','Two equal positive charges are symmetrically placed left and right of a target on the y-axis. Their net force points',['left','right','up or down along the symmetry axis','zero because each force is nonzero'],'c'),
 ('Coordinate components','For a source at $(x_s,y_s)$ and target $(x_t,y_t)$, form $\Delta x=x_t-x_s$, $\Delta y=y_t-y_s$, then divide the displacement vector by $r^3$. This prevents mixing a distance with a component.','A source at $(1,2)$ acts on a target at $(4,6)$. What is the displacement used in the numerator?',['$(1,2)$','$(4,6)$','$(3,4)$','$(5,8)$'],'c'),
 ('Units and Coulomb constant','Since $k$ has units $\mathrm{N\,m^2/C^2}$, $kq_1q_2/r^2$ has units newtons. Convert microcoulombs before numerical work and retain the factor $10^{-6}$ for each charge.','Which unit check is correct for $kq_1q_2/r^2$?',['C','N','N/C','N m'],'b'),
 ('Limits and model validity','As $r\to\infty$, a point-charge force tends to zero like $1/r^2$. As $r\to0$ the ideal model diverges; finite-size structure then matters. A limit check can expose a missing square or wrong sign.','Which behavior is consistent with Coulomb’s law for fixed nonzero charges?',['Force grows linearly with distance','Force approaches zero as distance grows','Force is independent of distance','Force changes sign when only distance changes'],'b')]},
'electric-fields-points': {
 'aid':'physics2-ch05-electric-fields-points-concept-lesson','title':'Electric Fields of Point Charges','bp':'physics2-point-charge-fields-calculus-v1','packet':'packet-physics2-point-charge-fields-calculus-v1',
 'skills':['electric-field','vector-superposition','test-charge-independence','inverse-square-law','unit-analysis'],
 'sections':[
 ('Field as force per charge','Define the electric field at a location by $\mathbf E=\mathbf F/q_0$ for a positive test charge taken small enough not to disturb the sources. The field belongs to the source arrangement; a test charge samples it.','A positive test charge placed where $\mathbf E$ points left experiences force',['left','right','zero','perpendicular to $\mathbf E$'],'a'),
 ('Point-charge field','For a source charge $q$ at $\mathbf r_s$, $\mathbf E(\mathbf r)=kq(\mathbf r-\mathbf r_s)/|\mathbf r-\mathbf r_s|^3$. Positive $q$ points away and negative $q$ points toward the source.','At a point to the right of a negative point charge, the field points',['right, away from the charge','left, toward the charge','upward','zero'],'b'),
 ('Field versus force','The field does not include the test charge: $\mathbf F=q_0\mathbf E$. Reversing the sign of $q_0$ reverses the force but leaves $\mathbf E$ unchanged.','If $\mathbf E$ points upward and $q_0<0$, the force on the test charge points',['upward','downward','zero','radially outward from the source'],'b'),
 ('Superposition and components','Fields from multiple sources add as vectors, $\mathbf E=\sum_i\mathbf E_i$. Resolve each displacement into components before adding; symmetry may cancel one component of the total, not of each contribution.','Two identical positive charges symmetric about the y-axis produce at a point on that axis a net field with',['horizontal components cancelling and vertical components adding','vertical components cancelling and horizontal components adding','both components cancelling everywhere','magnitudes added without direction'],'a'),
 ('Distance scaling','For one point charge, $|\mathbf E|=k|q|/r^2$. Doubling $r$ makes the field one-fourth, while doubling $|q|$ doubles it. State what is held fixed before using proportionality.','If the observation distance triples while $q$ stays fixed, $|\mathbf E|$ becomes',['three times larger','one-third as large','one-ninth as large','unchanged'],'c'),
 ('Units and field lines','Field units are N/C (equivalently V/m). Field-line direction is tangent to $\mathbf E$; line density is qualitative, while the inverse-square equation supplies magnitude.','Which expression has electric-field units?',['$kq/r^2$','$kq^2/r^2$','$kq/r$','$q/r^2$'],'a'),
 ('Transfer and limits','Use a consistent source/observer coordinate system, check signs and units, and test limits. A distant collection of charges behaves like net charge $Q$ to leading order, so $E\sim kQ/r^2$.','For fixed nonzero net charge viewed very far away, the field magnitude should',['approach zero like $1/r^2$','grow like $r^2$','stay constant','depend on the test charge'],'a')]}}

def block(v):
 class D(yaml.SafeDumper): pass
 def rep(d,x): return d.represent_scalar('tag:yaml.org,2002:str',x,style='|' if '\n' in x else ("'" if '\\' in x else None))
 D.add_representer(str,rep); return yaml.dump(v,Dumper=D,sort_keys=False,allow_unicode=True,width=110)

for key,cfg in configs.items():
 a=yaml.safe_load(yaml.safe_dump(base,sort_keys=False))
 a['id']=cfg['aid']; a['title']=cfg['title']; a['authoring']['sourcePacketId']=cfg['packet']; a['authoring']['blueprintId']=cfg['bp']; a['authoring']['visualRationale']='Original diagrams show source and observation coordinates, displacement vectors, and component directions.'; a['skills']=cfg['skills']; a['navigation']['tags']=['physics-2','physics2-electric-charges-fields','s2c-reviewed']
 secs=[]
 for i,(title,content,prompt,choices,ans) in enumerate(cfg['sections'],1):
  s={'id':f"{cfg['aid'].replace('-concept-lesson','')}-s{i}",'title':title,'required':True,'content':content,'media':[]}
  if i in (2,4,5,7):
   kind='point-charge' if key.startswith('electric') else 'coulomb'
   s['media']=[{'type':'image','src':f'/media/physics2/{kind}-model.svg','alt':f'Original diagram for {title}: source charges, target point, displacement vectors, and field or force directions.'}]
  old=base['lesson']['sections'][i-1]['check']; q=yaml.safe_load(yaml.safe_dump(old,sort_keys=False)); q['id']=f"{s['id']}-check"; q['prompt']=prompt; q['answer']['choiceId']=ans; q['choices']=[]
  for j,text in enumerate(choices):
   q['choices'].append({'id':chr(97+j),'text':text,'media':[],'issueSignals':([] if chr(97+j)==ans else old['choices'][j]['issueSignals'])})
  q['explanation']=f"Solution: Choice {ans.upper()} follows by applying the stated relation to the given signs, coordinates, or scaling.\n\nWhy it works: The governing equation and the prompt's condition determine the vector direction or magnitude without adding an unstated assumption.\n\nWhy the other choices fail: Each alternative confuses a source with a target, drops a vector component, uses the wrong distance exponent, or assigns incorrect units for this specific prompt."
  q['difficultyDimensions']=['modelOrDerivation','representationTransfer']; q['difficultyEvidence']=f"{title}: apply the governing electrostatics relation and verify the prompt-specific direction, scaling, or units."; s['check']=q; secs.append(s)
 a['lesson']['sections']=secs
 out=ROOT/'scratch'/f'{key}.yaml'; out.write_text(block(a),encoding='utf-8')
 print('*** Begin Patch')
 path=ROOT/f"data/assessments/{cfg['aid']}.yaml"; old=path.read_text().splitlines(); print(f'*** Update File: {path.as_posix()}'); print('@@'); print('\n'.join('-'+x for x in old)); print('\n'.join('+'+x for x in out.read_text().splitlines()))
 print('*** End Patch')
