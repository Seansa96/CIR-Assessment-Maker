"""Emit reviewable patches; source records and blueprints precede lesson materialization."""
from pathlib import Path
import json, sys, yaml
ROOT=Path(__file__).resolve().parents[1]
SID='src-20260806094518-3f5d8d0e38'
BASE=ROOT/'data/source-library/sources'/SID
aid='physics2-ch05-continuous-charge-concept-lesson'
draft=yaml.safe_load((ROOT/'scratch/continuous-charge-draft.yaml').read_text(encoding='utf-8'))
def emit(path,value):
    path=ROOT/path
    if path.exists():
        old=path.read_text(encoding='utf-8')
        print(f'*** Update File: {path.as_posix()}\n@@')
        for line in old.splitlines(): print('-'+line)
    else: print(f'*** Add File: {path.as_posix()}')
    for line in value.splitlines(): print('+'+line)
def js(value): return json.dumps(value,ensure_ascii=False,indent=2)+'\n'
notes={
202:'Visually reviewed PDF page 202, section 5.5: Continuous charge is an approximation for many discrete charges. Divide the source into differential pieces treated as point charges; combine their fields by superposition. Sources may occupy lines, surfaces, or volumes.',
203:'Visually reviewed PDF page 203: lambda has units C/m, sigma C/m^2, rho C/m^3. Replace point-charge sums by vector integrals with dq=lambda dl, sigma dA, or rho dV. Density can vary with position and must be expressed in source coordinates. Separation r runs from the source element to the fixed observation point P. Integrate each vector component; diagrams show cancellation of some components.',
204:'Visually reviewed PDF page 204: Uniform line segment of full length ell centered at the origin, observed a perpendicular distance z above its midpoint. Opposite source elements have equal horizontal and vertical component magnitudes; horizontal components cancel and vertical ones add. dq=lambda dx; paired integration uses twice the interval 0 to ell/2.',
205:'Visually reviewed PDF page 205: For the centered rod, r=sqrt(z^2+x^2) and cos(theta)=z/r. The field integrand is proportional to z dx/(z^2+x^2)^(3/2). An antiderivative of 1/(z^2+x^2)^(3/2) is x/(z^2 sqrt(z^2+x^2)). Endpoint evaluation gives k lambda ell/[z sqrt(z^2+ell^2/4)]. Do not double-count paired source elements. Infinite-line setup extends the source-coordinate limits to both infinities.',
206:'Visually reviewed PDF page 206: Infinite-line field is 2k lambda/z. For a finite rod at z much greater than its length, the result becomes kQ/z^2 with Q=lambda times full length. Increasing rod length at fixed lambda yields the infinite-line result. A uniform ring is introduced as the next example.',
207:'Visually reviewed PDF page 207: Ring radius R, observation on its axis at z. An arc has dl=R d(theta), dq=lambda R d(theta). Distance sqrt(R^2+z^2) and axial projection z/sqrt(R^2+z^2) are constant in the angle integral. Transverse components cancel. Integration from 0 to 2pi gives E_z=kQz/(R^2+z^2)^(3/2), approaching kQ/z^2 far away.',
208:'Visually reviewed PDF page 208: Uniform disk radius R and surface density sigma, observer at z>0. Use concentric annuli of variable radius s, with dA=2pi s ds, separation sqrt(s^2+z^2), axial projection z/sqrt(s^2+z^2). E_z=2pi k sigma z integral_0^R s ds/(s^2+z^2)^(3/2)=2pi k sigma(1-z/sqrt(R^2+z^2)). Source radius and source-to-observer distance are distinct.',
209:'Visually reviewed PDF page 209: Disk far-field expansion gives E_z approximately k sigma pi R^2/z^2, the field of Q=sigma pi R^2. Taking disk radius to infinity at fixed sigma gives sigma/(2 epsilon_0), directed away from a positive plane; below the plane the direction reverses.'}
support=[[202,203],[203],[203,204],[204,205],[206,207],[208],[203,206,209]]
principles=['Source-to-observer displacement in vector Coulomb superposition','Local density times line element and definite charge integration','Equal-charge component pairing at a fixed observation point','Endpoint subtraction after the rod antiderivative','Constant ring-axis distance with axial projection','Annular area and substitution with transformed limits','Parity of density-weighted components under broken reflection symmetry']
methods=[['Hold observer at (0,a).','Subtract (x,0) to obtain (-x,a).','Distinguish displacement vector from its scalar length.'],['Use dq=lambda0 x dx/L.','Integrate x from 0 to L.','Cancel L and verify charge units.'],['Write displacements (-x,a) and (x,a).','Factor their common positive Coulomb multiplier.','Sum vectors, cancelling horizontal components only.'],['Differentiate x/(a^2 sqrt(x^2+a^2)) to verify the primitive.','Subtract its values at -L and L.','Multiply by k lambda a without an extra doubling.'],['Use D=sqrt(2)R at z=R.','Project by z/D=1/sqrt(2).','Multiply kQ/D^2 by the projection.'],['Set u=z^2+s^2 and s ds=du/2.','Transform both endpoints.','Keep the orientation of increasing bounds.'],['Expand density-weighted horizontal and vertical integrands.','Discard odd terms over [-L,L].','Identify the surviving negative horizontal correction and zero vertical correction.']]
misconceptions=['Reversing the displacement or discarding an individual horizontal component','Treating endpoint density as constant or losing the integration scale factor','Adding magnitudes or cancelling both components from shape alone','Missing one endpoint, double-counting halves, or using a fixed distance','Omitting axial projection or using the center/far-field result at z=R','Omitting the substitution factor or retaining/reversing original bounds','Confusing symmetric geometry with symmetric charge and reversing the right-side contribution']
signatures=['coulomb-source-observer-displacement-rod-element','linear-density-charge-normalization-endpoint-vs-average','paired-positive-elements-component-vector-addition','finite-centered-rod-antiderivative-two-endpoints','ring-axis-one-radius-distance-and-projection','disk-annulus-u-substitution-jacobian-bounds','affine-density-centered-rod-even-odd-component-correction']
print('*** Begin Patch')
if sys.argv[1]=='sources':
    chunks=json.loads((BASE/'chunks.json').read_text(encoding='utf-8'))
    assert not any(c['id']==f'{SID}:page-{p:04}' for c in chunks for p in notes)
    for p,note in notes.items():
        chunks.append(dict(id=f'{SID}:page-{p:04}',ordinal=100000+p,kind='page-image',locator=f'PDF page {p}',text=note,tokenCount=len(note.split()),ocrConfidence=None,imagePath=f'page-images/page-{p:04}.png',pageNumber=p,transcriptionReviewState='approved'))
    manifest=json.loads((BASE/'manifest.json').read_text(encoding='utf-8')); manifest['chunkCount']=len(chunks)
    original=(BASE/'chunks.json').read_text(encoding='utf-8').splitlines()
    print(f'*** Update File: {(BASE/"chunks.json").as_posix()}\n@@')
    tail=original[-14:]
    for line in tail: print('-'+line)
    replacement='\n'.join(tail).rstrip()
    # Retain the final old object and append reviewed records before the outer bracket.
    replacement=replacement[:replacement.rfind(']')].rstrip()+',\n'+',\n'.join(json.dumps(c,ensure_ascii=False,indent=2) for c in chunks[-len(notes):])+'\n]'
    for line in replacement.splitlines(): print('+'+line)
    emit(f'data/source-library/sources/{SID}/manifest.json',js(manifest))
    packet=dict(schemaVersion=1,id=draft['authoring']['sourcePacketId'],sourceId=SID,curriculumId='physics-2-calculus-curriculum',categoryId='physics-2',topicId=draft['topicId'],objectiveIds=['physics2-ch05-electric-charges-fields-continuous-charge-fields'],chunkIds=[f'{SID}:page-{p:04}' for p in notes],reviewState='approved',reviewNotes='PDF pages visually reviewed; original.pdf SHA256 matches manifest. These reviewed page-image summaries replace inadequate chapter-opening evidence for this assessment only.',outputConstraints=dict(verbatimSourceTextExcluded=True,requireOriginalVisuals=True,requireStructuredExplanations=True))
    emit('docs/assessment-reference/packets/packet-physics2-continuous-charge-calculus-v1.json',js(packet))
    rows=[]
    for i,s in enumerate(draft['lesson']['sections']):
        q=s['check']
        rows.append(dict(id=q['id']+'-blueprint',assessmentId=aid,questionId=q['id'],objectiveId=packet['objectiveIds'][0],sourceChunks=[f'{SID}:page-{p:04}' for p in support[i]],reviewState='approved',questionType='multipleChoice',givens=q['prompt'],unknown=q['choices'][ord(q['answer']['choiceId'])-97]['text'],representationRequirement='Use the coordinates, positive-parameter conditions, and geometric source element specified in the prompt.',governingPrinciple=principles[i],methodSteps=methods[i],likelyMisconception=misconceptions[i],difficultyDimensions=['modelOrDerivation','errorDiagnosis'],difficultyEvidence=principles[i]+': '+methods[i][-1],answerVerificationMethod='; '.join(methods[i]),variationAxes=['representation','unknown','method branch'],reasoningSignature=signatures[i]))
    emit('docs/assessment-reference/question-blueprints/physics2-continuous-charge-calculus-v1.yaml',yaml.safe_dump(dict(schemaVersion=1,id=draft['authoring']['blueprintId'],categoryId='physics-2',topicId=draft['topicId'],packetId=packet['id'],reviewState='approved',blueprints=rows),sort_keys=False,allow_unicode=True))
elif sys.argv[1]=='lesson':
    old=yaml.safe_load((ROOT/f'data/assessments/{aid}.yaml').read_text(encoding='utf-8'))
    assert [s['id'] for s in old['lesson']['sections']]==[s['id'] for s in draft['lesson']['sections']]
    assert [s['check']['id'] for s in old['lesson']['sections']]==[s['check']['id'] for s in draft['lesson']['sections']]
    for i,s in enumerate(draft['lesson']['sections']):
        s['check']['difficultyDimensions']=['modelOrDerivation','errorDiagnosis']; s['check']['difficultyEvidence']=principles[i]+': '+methods[i][-1]
        if i in [2,3,4,5]:
            name='rod' if i in [2,3] else ('ring' if i==4 else 'disk')
            s['media']=[dict(type='image',src=f'/media/physics2/continuous-charge-{name}.svg',alt={'rod':'Rod on the x-axis from minus L to L, with observer P at (0,a), charge elements at plus and minus x, and source-to-observer displacement arrows.','ring':'Ring in the xy-plane of radius R with observer P at height z, an arc charge element, separation D, and axial field direction.','disk':'Disk of radius R with a highlighted annulus of radius s and thickness ds; observer P is height z above the center.'}[name])]
    class BlockDumper(yaml.SafeDumper): pass
    def string(dumper,value): return dumper.represent_scalar('tag:yaml.org,2002:str',value,style='|' if '\n' in value else ("'" if '\\' in value else None))
    BlockDumper.add_representer(str,string)
    emit(f'data/assessments/{aid}.yaml',yaml.dump(draft,Dumper=BlockDumper,sort_keys=False,allow_unicode=True,width=110))
print('*** End Patch')
