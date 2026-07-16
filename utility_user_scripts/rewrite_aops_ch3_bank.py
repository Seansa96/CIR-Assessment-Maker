from pathlib import Path
import yaml
Q=[
('Solve $3x-7=14$','x=7'),('Solve $5-2x=17$','x=-6'),('Solve $4(x-3)=2x+6$','x=9'),('Solve $x/3+5=9$','x=12'),('Solve $7(x+1)-2=3x+18$','x=13/2'),('Classify $4x+2=4x+2$','infinitely many solutions'),('Classify $3x-5=3x+1$','no solution'),('Find the slope through $(2,3)$ and $(6,11)$','2'),('Solve $x+y=9$, $x-y=1$','x=5,y=4'),('Solve $2x+y=7$, $x-y=2$','x=3,y=1'),('Does $(2,-1)$ satisfy $3x+2y=4$?','yes'),('Write an equation with slope -3 through $(1,4)$','y-4=-3(x-1)'),
('Solve $3(x-2)=2(x+5)+x$','no solution'),('Solve $2(x+1)-3=5x-6$','x=5/3'),('A taxi costs $4 plus $2.50 per mile; cost is $19$. Miles?','6'),('Two consecutive integers sum to 41. Find them.','20,21'),('A rectangle has perimeter 34 and length 3 more than width. Find dimensions.','10,7'),('Solve $x/2+y/3=4$ and $x+y=9$','x=6,y=3'),('Find intersection of $y=2x+1$ and $y=7-x$','(2,5)'),('A mixture has 3 kg more water than juice and totals 17 kg. Find each.','water=10,juice=7'),('What operation eliminates y from $4x+3y=8$ and $2x-3y=10$?','add equations'),('Solve $0.2x+1.5=2.7$','x=6'),('A number increased by 8 is twice itself minus 1. Find it.','9'),('Solve $|x-4|=7$','x=11,-3'),('Explain why $x=0$ must be checked before dividing an equation by x.','division by zero can discard a case'),('Solve $3x+2y=12$, $6x+4y=24$','infinitely many solutions'),('Solve $x+y=4$, $2x+2y=11$','no solution'),('A 120-mile trip takes 2 hours partly at 50 mph and partly at 70 mph. Times?','1 hour each'),
('Prove an equation has at most one solution when it simplifies to $ax=b$ with $a\\ne0$.','division by nonzero a gives one value'),('Give a counterexample to “two equations always have one intersection.”','parallel distinct lines'),('Choose substitution or elimination for $y=3x-2$ and $4x+y=9$.','substitution'),('Explain the invariant in solving an equation.','both sides remain equal'),('A solution obtained x=-2 for a count. What must be decided?','whether context permits it'),('Derive the distance-rate-time equation from units.','distance=rate times time'),('Why can multiplying an equation by zero destroy information?','both sides become 0'),('Create a system with solution $(1,2)$.','any two independent lines through point'),('Explain why a check uses original equations.','transformations may introduce errors'),('A store discounts 20% then adds $6 tax; write cost from price p.','0.8p+6'),('Identify the unknowns before modeling a coin problem.','counts of each coin'),('Describe a graphical meaning of no solution in a system.','distinct parallel lines')]
Q[4] = (Q[4][0], 'x=13/4')
tiers=['foundational']*12+['multi-step']*16+['contest-transfer']*8+['proof-strategy']*4
outlines=[
'Add 7 and divide by 3; substitute 7 back.', 'Subtract 5 and divide by -2.', 'Distribute, collect x terms, then isolate x.', 'Subtract 5, then multiply the entire equation by 3.',
'Expand first and collect like terms.', 'Cancel 4x to obtain the identity 2=2.', 'Cancel 3x to obtain the contradiction -5=1.', 'Use rise over run: (11-3)/(6-2).',
'Add the two equations, then recover y.', 'Substitute y=x-2 into 2x+y=7.', 'Plug both coordinates into the equation.', 'Use point-slope form with (1,4).',
'Expand; cancellation leaves unequal constants.', 'Simplify the left side before moving terms.', 'Model cost as 4+2.5m=19.', 'Let the integers be n and n+1.',
'Let width be w and use 2w+2(w+3)=34.', 'Clear denominators, then solve with x+y=9.', 'Set 2x+1 equal to 7-x.', 'Let juice be j and water be j+3.',
'Add because 3y and -3y cancel.', 'Subtract 1.5 and divide by 0.2.', 'Write n+8=2n-1 before solving.', 'Solve the positive and negative absolute-value cases.',
'State that division by zero is undefined and may discard cases.', 'Recognize the second equation as twice the first.', 'Compare 2 times the first equation with the second.', 'Let t be time at 50 mph and use 50t+70(2-t)=120.',
'Divide ax=b by the nonzero a to get x=b/a.', 'Name distinct parallel lines as the counterexample.', 'Use substitution because y is already isolated.', 'State that reversible steps preserve exactly the solution set.',
'Compare the algebraic result with the quantity being counted.', 'Multiply rate units (distance/time) by time.', 'Explain that both sides become zero regardless of the original relation.', 'Give two nonparallel equations through (1,2).',
'Substitute into the original, not merely a simplified line.', 'Translate 20% off as 0.8p, then add 6.', 'Define variables as the two coin counts.', 'Describe equal slopes with different intercepts.'
]
traps=[
'Dividing before undoing subtraction.', 'Dropping the negative sign.', 'Forgetting to distribute.', 'Treating x/3+5 as (x/3+5)/3.',
'Combining unlike terms.', 'Calling an identity one solution.', 'Calling a contradiction infinitely many solutions.', 'Using x/y instead of coordinate differences.',
'Stopping after x.', 'Using y=x+2.', 'Checking only one coordinate.', 'Treating 4 as an intercept.',
'Dividing by a vanished coefficient.', 'Moving a term with the wrong sign.', 'Omitting the fixed fee.', 'Using n and n+2.',
'Using area rather than perimeter.', 'Multiplying only one term by 6.', 'Averaging expressions for y.', 'Giving the extra 3 kg to both amounts.',
'Subtracting and doubling y.', 'Treating .2 as 2.', 'Writing 8n.', 'Keeping one branch only.',
'Assuming x can be cancelled.', 'Reporting one point.', 'Calling proportional equations inconsistent.', 'Using average speed without time variables.',
'Forgetting a must be nonzero.', 'Giving coincident lines.', 'Choosing elimination by habit.', 'Preserving equality but not solutions.',
'Accepting a negative count.', 'Adding incompatible units.', 'Thinking 0=0 proves the original equation.', 'Choosing parallel lines.',
'Checking a transformed equation only.', 'Discounting the tax too.', 'Using dollar values instead of counts.', 'Saying simply that lines do not cross.'
]
assert len(Q)==len(outlines)==len(traps)==40
items=[]
for i, ((p,a), outline, trap) in enumerate(zip(Q,outlines,traps),1):
    items.append({'id':f'aops-v1-ch03-q{i:03d}','skillIds':['apply-linear-equations','verify-linear-equations-solutions'],'archetype':['isolate','system','model','classification','proof'][i%5],'difficulty':tiers[i-1],'questionType':'freeResponse','prompt':p,'answer':a,'solutionOutline':outline,'commonTrap':trap,'intendedUse':'quiz-test-bank'})
doc={'metadata':{'id':'aops-v1-ch03-linear-equations-bank','title':'AoPS Volume 1 Chapter 3: Linear Equations Question Bank','chapter':3,'topicIds':['aops-linear-equations'],'sourcePageRange':'pdf 31-41; printed 17-27','originalAuthoring':True,'distribution':{'foundational':12,'multi-step':16,'contest-transfer':8,'proof-strategy':4}},'items':items}
Path('docs/assessment-reference/aops-volume-1/chapter-03-linear-equations-question-bank.yaml').write_text(yaml.safe_dump(doc,sort_keys=False,allow_unicode=True),encoding='utf8')
