from pathlib import Path
import yaml

Q=[
('Factor $x^2-49$.','$(x-7)(x+7)$','Apply the difference-of-squares identity.','Using $(x-49)(x+1).'),
('Factor $8a^3-27$.','$(2a-3)(4a^2+6a+9)$','Recognize $(2a)^3-3^3$.','Using a minus sign in the quadratic factor.'),
('Factor $x^3+125$.','$(x+5)(x^2-5x+25)$','Recognize a sum of cubes.','Making both signs positive.'),
('Evaluate $1003^2-997^2$.','12000','Use $(1003-997)(1003+997)$.','Squaring both large numbers first.'),
('Expand $(a-b)^2$.','$a^2-2ab+b^2$','Square the binomial or multiply it by itself.','Using plus 2ab.'),
('Simplify $x^2+6x+9$.','$(x+3)^2$','It is a perfect-square trinomial.','Factoring as $(x+9)(x+1).'),
('Factor $27y^3+8$.','$(3y+2)(9y^2-6y+4)$','Use $(3y)^3+2^3$.','Using $(3y-2)$.') ,
('If $a+b=10$ and $ab=21$, find $a^2+b^2$.','58','Square the sum and subtract 2ab.','Computing $10^2-21$.'),
('If $x+1/x=5$, find $x^2+1/x^2$.','23','Square the given relation and subtract 2.','Squaring each term but omitting the cross term.'),
('Factor $16m^4-n^4$.','$(4m^2-n^2)(4m^2+n^2)$','First use a difference of squares.','Treating it as a difference of cubes.'),
('Is $a^2+b^2=(a+b)(a-b)$?','No','Expand the right side to get $a^2-b^2$.','Trusting visual similarity.'),
('Factor $x^3-x$.','$x(x-1)(x+1)$','Factor x, then factor a difference of squares.','Stopping at x times $(x^2-1)$.') ,
('Evaluate $51^2-49^2$.','200','Use $(51-49)(51+49)$.','Treating it as $(2)^2.'),
('Factor $2x^3+16$.','$2(x+2)(x^2-2x+4)$','Factor 2, then use sum of cubes.','Forgetting the common factor.'),
('If $p+q=7$ and $pq=10$, find $p^3+q^3$.','133','Use $(p+q)^3-3pq(p+q)$.','Using $7^3-10$.'),
('Simplify $(x+4)^2-(x-4)^2$.','16x','Treat as a difference of squares with factors 8 and 2x.','Expanding only one square.'),
('Factor $a^4-16$.','$(a-2)(a+2)(a^2+4)$','Use difference of squares twice.','Factoring $a^2+4$ over the reals.'),
('If $r+1/r=3$, find $r^3+1/r^3$.','18','Cube the sum: $27=r^3+1/r^3+9$.','Using 27-3.'),
('Factor $x^3-8y^3$.','$(x-2y)(x^2+2xy+4y^2)$','Use difference of cubes.','Using a negative middle term.'),
('Find $99^2$ without ordinary multiplication.','9801','Use $(100-1)^2=10000-200+1$.','Using $10000-1$.'),
('If $u-v=4$ and $uv=3$, find $u^2+v^2$.','22','Square $u-v$: 16 equals sum of squares minus 6.','Subtracting 6 rather than adding it.'),
('Simplify $\frac{x^2-1}{x-1}$ for $x\ne1$.','$x+1$','Factor numerator and cancel the factor only under its restriction.','Claiming the result is defined at x=1.'),
('Factor by grouping: $ax+ay+bx+by$.','$(a+b)(x+y)$','Group first two and last two terms, then factor common binomial.','Cancelling a or b.'),
('If $z+1/z=4$, find $z^2+1/z^2$.','14','Square and subtract 2.','Using 16-1.'),
('Find $1001\cdot999$.','999999','Use $(1000+1)(1000-1)$.','Multiplying 1001 by 999 directly.'),
('Why is $(x+y)(x-y)$ not a factorization of $x^2+y^2$?','It expands to $x^2-y^2$.','Expand to check the claimed identity.','Saying it fails only for negative inputs.'),
('Find all real x satisfying $x^4-13x^2+36=0$.','$x=\pm2,\pm3$','Let u=x squared and factor $(u-4)(u-9)$.','Reporting u=4,9 as x values.'),
('If a+b=6 and a squared+b squared=20, find ab.','8','Square the sum: 36=20+2ab.','Using 36-20 without dividing by 2.'),
('Simplify $(x^2+x+1)(x-1)$.','$x^3-1$','Distribute and observe cancellation.','Calling it $x^3+1$.'),
('A positive x satisfies x+1/x=2. Find x.','1','Equality case: $(x-1)^2/x=0$, or solve $x^2-2x+1=0$.','Giving x=-1.'),
('Prove $a^3-b^3$ is divisible by a-b.','Use $a^3-b^3=(a-b)(a^2+ab+b^2)$.','Exhibit the quotient.','Testing a few numerical cases only.'),
('Explain why $x\ne0$ is required before multiplying $x+1/x=5$ by x.','The original reciprocal is undefined at zero.','Record the domain before a transformation.','Assuming multiplication makes zero harmless.'),
('Give a counterexample to cancelling x in $x(x-1)=x(x-2)$.','x=0 satisfies both originals but not $x-1=x-2$.','Use the zero factor that cancellation would discard.','Choosing nonzero x.'),
('Choose a fast method for $1000001^2-999999^2$.','Use difference of squares to get $4,000,000$.','Recognize the numbers as 1,000,000 plus/minus 1.','Subtracting the bases before squaring.'),
('Why does knowing a+b and ab often suffice for symmetric expressions?','Many can be rewritten using elementary symmetric quantities, such as $a^2+b^2=(a+b)^2-2ab$.','Name the rewrite.','Claiming it determines a and b uniquely.'),
('Find $a^4+b^4$ if a+b=3 and ab=1.','47','First get $a^2+b^2=7$, then square and subtract $2a^2b^2$.','Using $7^2-2$ without explaining the square.'),
('Construct two distinct real numbers with sum 5 and product 6.','2 and 3','Use roots of $t^2-5t+6$.','Giving 1 and 4.'),
('When does $a^2-b^2=0$ imply a=b?','Only with extra conditions; in general a=\pm b.','Factor $(a-b)(a+b)=0$.','Ignoring the a=-b branch.'),
('Verify the sum-of-cubes identity by expansion.','$(a+b)(a^2-ab+b^2)=a^3+b^3$.','Distribute every term and cancel.','Leaving an uncancelled ab squared term.'),
('Explain a purposeful “add zero” move for $x^2+6x$.','Add and subtract 9 to create $(x+3)^2-9$.','Create a useful square without changing value.','Adding 6 because it is visible.')]
tiers=['foundational']*12+['multi-step']*16+['contest-transfer']*8+['proof-strategy']*4
assert len(Q)==40
items=[{'id':f'aops-v1-ch07-q{i:03d}','skillIds':['recognize-special-factorizations','manipulate-symmetric-expressions'],'archetype':['identity','symmetry','reciprocal','grouping','proof'][i%5],'difficulty':tiers[i-1],'questionType':'freeResponse','prompt':p,'answer':a,'solutionOutline':o,'commonTrap':t,'intendedUse':'quiz-test-bank'} for i,(p,a,o,t) in enumerate(Q,1)]
doc={'metadata':{'id':'aops-v1-ch07-special-factorizations-bank','title':'AoPS Volume 1 Chapter 7: Special Factorizations Question Bank','chapter':7,'topicIds':['aops-special-factorizations'],'sourcePageRange':'pdf 81-88; printed 67-74','originalAuthoring':True,'distribution':{'foundational':12,'multi-step':16,'contest-transfer':8,'proof-strategy':4}},'items':items}
Path('docs/assessment-reference/aops-volume-1/chapter-07-special-factorizations-question-bank.yaml').write_text(yaml.safe_dump(doc,sort_keys=False,allow_unicode=True),encoding='utf8')
