from pathlib import Path
import yaml
Q=[
('Classify -7 in the smallest listed set: natural, integer, rational, real, complex.','integer','It is negative but has no fractional part.','Calling every negative number irrational.'),
('Classify $3/8$ in the smallest listed set.','rational','It is a quotient of two integers with nonzero denominator.','Calling it an integer.'),
('Classify $\sqrt{49}$ in the smallest listed set.','natural number','It equals 7.','Classifying by the radical symbol alone.'),
('Classify $\sqrt2$ in the smallest listed set.','irrational real','It is real but not rational.','Calling every square root complex.'),
('Write 0.375 as a fraction in lowest terms.','$3/8$','Use 375/1000 and reduce.','Stopping before reduction.'),
('Write $0.\overline{6}$ as a fraction.','$2/3$','Let x=.666..., then 10x-x=6.','Writing 6/10.'),
('Is $0.1010010001\ldots$ rational?','No, assuming the displayed gaps continue growing.','Its nonrepeating pattern cannot be eventually periodic.','Calling it irrational merely because it is long.'),
('Which is larger: $5/12$ or $3/7$?','$3/7$','Cross multiply positive denominators: 35 versus 36.','Comparing only numerators.'),
('Write $-2.4$ as a lowest-terms fraction.','$-12/5$','Convert -24/10 and reduce.','Dropping the sign.'),
('Is 0 rational?','Yes','Use 0/1.','Thinking a rational number must be nonzero.'),
('Can a denominator in a rational representation be zero?','No','Division by zero is undefined.','Using 1/0 as infinity.'),
('Classify $4+3i$ in the smallest listed set.','complex nonreal','Its imaginary component is nonzero.','Calling it real because 4 is real.'),
('Write $0.\overline{27}$ as a fraction.','$3/11$','Let x=.2727..., then 100x-x=27.','Using 27/100.'),
('Write $1.2\overline{3}$ as a fraction.','$37/30$','Shift past the nonrepeating digit, then subtract: 100x-10x=111.','Treating all digits as repeating.'),
('Prove that the sum of a rational and an irrational is irrational.','If r+x were rational, subtracting rational r would make x rational, contradiction.','Use closure of rationals under subtraction.','Claiming examples alone prove it.'),
('Give two irrational numbers whose sum is rational.','$\sqrt2$ and $-\sqrt2$','Their sum is 0.','Choosing two positives without checking sum.'),
('Give two irrational numbers whose product is rational.','$\sqrt2$ and $\sqrt2$','Their product is 2.','Assuming irrational products are always irrational.'),
('Is $\sqrt{18}$ rational?','No','Simplify to $3\sqrt2$ and use irrationality of sqrt2.','Saying 18 is not a perfect square without explanation.'),
('Find the smallest set containing $-i$.','complex','It is not real.','Calling it irrational.'),
('Explain why every integer is rational.','n=n/1.','Give a valid nonzero denominator.','Using n/0.'),
('Reduce $84/126$ to lowest terms.','$2/3$','Divide numerator and denominator by gcd 42.','Dividing by different factors.'),
('Does $0.125$ terminate in base ten?','Yes','It has finitely many decimal digits.','Confusing it with a repeating decimal.'),
('What denominator forms allow a lowest-terms rational number to terminate in base ten?','Only powers of 2 times powers of 5.','A terminating decimal denominator divides a power of 10.','Saying any even denominator works.'),
('Prove $\sqrt2$ is irrational in outline.','Assume lowest p/q; p squared=2q squared forces p and q even, contradiction.','Use parity and lowest terms.','Skipping why p even forces q even.'),
('Which is larger: $7/15$ or $11/24$?','$7/15$','Compare 7 times 24=168 with 11 times 15=165.','Comparing denominators alone.'),
('If x is rational and nonzero, is 1/x rational?','Yes','If x=p/q, then 1/x=q/p.','Forgetting x cannot be zero.'),
('Is $\sqrt{a^2}$ always a?','No; it is $|a|$ for real a.','Test a negative value.','Dropping absolute value.'),
('Find a rational between $\sqrt2$ and $3/2$.','$7/5$','Check 1.4 squared is below 2 and 1.5 is above it.','Using a decimal without verifying bounds.'),
('Why does a repeating decimal represent a rational number?','A power-of-ten shift and subtraction produce an integer equation for it.','Describe the algebraic mechanism.','Saying repetition makes it a fraction by definition.'),
('Classify $\sqrt{-9}$ in the complex system.','3i or -3i are square roots; it is nonreal complex.','Use i squared=-1.','Saying the expression has no meaning when complex numbers are allowed.'),
('Prove that a rational in lowest terms cannot have numerator and denominator both even.','They would share factor 2, contradicting lowest terms.','Apply the definition.','Saying even fractions do not exist.'),
('Give a counterexample to “the difference of two irrational numbers is irrational.”','$\sqrt2-\sqrt2=0$.','Produce a rational difference.','Using two unrelated irrationals without computing.'),
('Choose a proof approach for irrationality of $\sqrt{12}$.','Reduce to $2\sqrt3$, then use the prime-factor contradiction for sqrt3.','Connect to a nonsquare prime factor.','Trying decimal approximation.'),
('Why must a rational representation use integers p and q?','The definition concerns a ratio of integers; allowing arbitrary reals would classify every real as x/1.','State why the restriction has content.','Saying fractions visually have integers.'),
('If r is rational and x is irrational, can rx be rational when r is nonzero?','No','Otherwise divide by nonzero rational r to make x rational.','Forgetting the nonzero condition.'),
('Give a counterexample showing irrational times irrational need not be irrational.','$\sqrt2\cdot\sqrt2=2$.','Compute the product exactly.','Giving a sum example.'),
('Explain the real-versus-complex distinction for $x^2+1=0$.','No real x squares to -1, but complex roots are i and -i.','Name the permitted number system.','Saying it has both roots in the reals.'),
('Find the decimal form of $7/40$.','0.175','Scale denominator to 1000.','Writing .17 repeating.'),
('Verify that $0.\overline{09}=1/11$.','Multiply by 100 and subtract x: 99x=9.','Use the repeated block length.','Using 9/100.'),
('Why is a calculator approximation insufficient to prove irrationality?','Finite displays cannot establish a decimal never terminates or repeats.','Distinguish evidence from proof.','Treating many digits as a proof.')]
tiers=['foundational']*12+['multi-step']*16+['contest-transfer']*8+['proof-strategy']*4
assert len(Q)==40
items=[{'id':f'aops-v1-ch08-q{i:03d}','skillIds':['classify-number-sets','prove-irrationality'],'archetype':['classify','decimal','closure','proof','restriction'][i%5],'difficulty':tiers[i-1],'questionType':'freeResponse','prompt':p,'answer':a,'solutionOutline':o,'commonTrap':t,'intendedUse':'quiz-test-bank'} for i,(p,a,o,t) in enumerate(Q,1)]
doc={'metadata':{'id':'aops-v1-ch08-number-systems-bank','title':'AoPS Volume 1 Chapter 8: Number Systems Question Bank','chapter':8,'topicIds':['aops-number-systems'],'sourcePageRange':'pdf 89-94; printed 75-80','originalAuthoring':True,'distribution':{'foundational':12,'multi-step':16,'contest-transfer':8,'proof-strategy':4}},'items':items}
Path('docs/assessment-reference/aops-volume-1/chapter-08-number-systems-question-bank.yaml').write_text(yaml.safe_dump(doc,sort_keys=False,allow_unicode=True),encoding='utf8')
