from pathlib import Path
import yaml

Q=[
('Solve $x^2-9=0$.','$x=\pm3$','Factor as $(x-3)(x+3)$.','Giving one root.'),
('Solve $x^2-5x+6=0$.','$x=2,3$','Factor using product 6 and sum -5.','Using factors that add to 5.'),
('Solve $x^2+7x+12=0$.','$x=-3,-4$','Factor as $(x+3)(x+4)$.','Dropping negative roots.'),
('Solve $2x^2-8=0$.','$x=\pm2$','Divide by 2 then take both square roots.','Taking only positive square root.'),
('Find the discriminant of $3x^2-4x+5=0$.','-44','Compute $(-4)^2-4(3)(5)$.','Using b instead of b squared.'),
('How many real roots has $x^2+4x+4=0$?','One repeated root','The discriminant is zero.','Calling it two distinct roots.'),
('Solve $x^2+1=0$ over the complex numbers.','$x=\pm i$','Move 1 and take complex square roots.','Reporting no roots in the stated universe.'),
('Write a monic quadratic with roots 2 and -5.','$x^2+3x-10=0$','Use $(x-2)(x+5)$.','Using the roots as coefficients directly.'),
('Find the sum of roots of $4x^2-7x+2=0$.','$7/4$','Use $-b/a$.','Using $b/a$.'),
('Find the product of roots of $4x^2-7x+2=0$.','$1/2$','Use $c/a$.','Using $-c/a$.'),
('Solve $x^2=49$.','$x=\pm7$','Take both square roots.','Writing x=7 only.'),
('Factor $x^2-16$.','$(x-4)(x+4)$','Use difference of squares.','Writing $(x-16)(x+1)$.'),
('Solve $x^2-2x-8=0$.','$x=4,-2$','Factor as $(x-4)(x+2)$.','Choosing factors with wrong product.'),
('Solve $3x^2+x-2=0$.','$x=2/3,-1$','Factor as $(3x-2)(x+1)$.','Forgetting to set each factor to zero.'),
('Solve $x^2+2x-7=0$.','$x=-1\pm2\sqrt2$','Use the quadratic formula.','Using discriminant 2 instead of 32.'),
('Solve $5x^2-20x=0$.','$x=0,4$','Factor out 5x.','Dividing by x and losing zero.'),
('Solve $x^4-5x^2+4=0$.','$x=\pm1,\pm2$','Let u=x squared and factor $u^2-5u+4$.','Keeping u roots as x roots.'),
('Solve $(x-1)^2=9$.','$x=4,-2$','Take both roots of the squared expression.','Adding 1 to only one branch.'),
('Find the vertex x-coordinate of $x^2-6x+1$.','3','Use $-b/(2a)$.','Using b/(2a).'),
('Complete the square: $x^2+8x+\_$.','16','Half of 8 is 4, then square it.','Adding 8.'),
('Solve $x^2+6x+5=0$ by completing the square.','$x=-1,-5$','Rewrite $(x+3)^2=4$.','Forgetting to subtract 9 from both sides.'),
('A rectangle has area 48 and length x+2, width x. Find positive x.','6','Set x(x+2)=48 and reject the negative root.','Keeping x=-8 as a length.'),
('Solve $\sqrt{x+5}=x-1$.','$x=4$','Require x>=1, square, then check candidates.','Keeping the extraneous root -1.'),
('Solve $1/x+1/(x-2)=3/4$.','$x=4,2/3$','Clear denominators after noting x is not 0 or 2.','Accepting a forbidden denominator.'),
('If roots are 3 and 7, form a quadratic with leading coefficient 2.','$2x^2-20x+42=0$','Start with $2(x-3)(x-7)$.','Forgetting the leading coefficient affects all terms.'),
('Find real k so $x^2+kx+9=0$ has one real root.','$k=\pm6$','Set discriminant $k^2-36$ to zero.','Setting k itself to 36.'),
('Explain why $x^2+2x+5=0$ has no real root.','Its discriminant is -16.','Use discriminant sign.','Saying it cannot factor over integers.'),
('Solve $2^{2x}-5\cdot2^x+6=0$.','$x=1,\log_2 3$','Let u=2 to the x and solve $(u-2)(u-3)=0$.','Allowing a negative u value.'),
('Find the sum of squares of roots of $x^2-5x+1=0$.','23','Use $(r+s)^2-2rs=25-2$.','Squaring each coefficient.'),
('A ball has height $-5t^2+20t+25$. When does it hit ground?','5 seconds','Set height zero and factor -5$(t-5)(t+1)$.','Keeping negative time.'),
('Prove a monic quadratic with roots r,s equals $x^2-(r+s)x+rs$.','Expand $(x-r)(x-s)$.','Use expansion as the proof.','Writing a signless middle term.'),
('Why can squaring create extraneous roots?','It makes $A=B$ and $A=-B$ indistinguishable.','Compare the reversible and nonreversible directions.','Claiming squaring always preserves equivalence.'),
('Give an equation with discriminant 0 and root 4.','$(x-4)^2=0$','Use a repeated linear factor.','Giving two distinct factors.'),
('Choose a method for $x^2+11x+7=0$ and justify it.','Quadratic formula; integer factoring is unavailable.','Compare factor pairs of 7 with required sum.','Factoring by guessing decimals.'),
('Explain why a real-coefficient quadratic with nonreal root a+bi also has a-bi.','The formula has real part $-b/(2a)$ and opposite imaginary signs.','Use the conjugate form from a negative discriminant.','Calling it true for arbitrary complex coefficients.'),
('If r+s=10 and rs=21, find $r^2+s^2$.','58','Compute $(r+s)^2-2rs$.','Using 100-21.'),
('Construct a quadratic whose roots are reciprocal nonzero numbers with sum 5.','$x^2-5x+1=0$','Their product is 1.','Using constant -1.'),
('Why must $a\ne0$ in a quadratic $ax^2+bx+c$?','Otherwise the x-squared term vanishes and degree is at most one.','Use the definition of degree.','Saying division by a is inconvenient.'),
('Verify that $x=3$ is not a root of $x^2-5x+5$.','Substitution gives -1, not 0.','Evaluate the original polynomial.','Checking a different equation.'),
('Give a counterexample to “a negative discriminant means no solutions.”','$x^2+1=0$ has $\pm i$ as complex roots.','Change the number system to complex numbers.','Using a quadratic with positive discriminant.')]
tiers=['foundational']*12+['multi-step']*16+['contest-transfer']*8+['proof-strategy']*4
assert len(Q)==40
items=[{'id':f'aops-v1-ch06-q{i:03d}','skillIds':['solve-quadratic-equations','verify-quadratic-solutions'],'archetype':['factor','formula','discriminant','substitution','proof'][i%5],'difficulty':tiers[i-1],'questionType':'freeResponse','prompt':p,'answer':a,'solutionOutline':o,'commonTrap':t,'intendedUse':'quiz-test-bank'} for i,(p,a,o,t) in enumerate(Q,1)]
doc={'metadata':{'id':'aops-v1-ch06-quadratic-equations-bank','title':'AoPS Volume 1 Chapter 6: Quadratic Equations Question Bank','chapter':6,'topicIds':['aops-quadratic-equations'],'sourcePageRange':'pdf 66-80; printed 52-66','originalAuthoring':True,'distribution':{'foundational':12,'multi-step':16,'contest-transfer':8,'proof-strategy':4}},'items':items}
Path('docs/assessment-reference/aops-volume-1/chapter-06-quadratic-equations-question-bank.yaml').write_text(yaml.safe_dump(doc,sort_keys=False,allow_unicode=True),encoding='utf8')
