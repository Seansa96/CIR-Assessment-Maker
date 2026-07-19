from pathlib import Path
import yaml

Q = [
('List the positive divisors of 18.','1, 2, 3, 6, 9, 18','Pair factors of 18 systematically.','Listing 18 twice or omitting 1.'),
('Is 1 prime, composite, or neither?','Neither','Use the definition: a prime has exactly two positive divisors.','Calling 1 prime because it has no nontrivial factors.'),
('Find the prime factorization of 360.','$2^3\cdot3^2\cdot5$','Divide by small primes until every factor is prime.','Stopping at 12 times 30.'),
('Find $\gcd(84,126)$.','42','Use common prime powers: $2\cdot3\cdot7$.','Taking the larger exponent for a gcd.'),
('Find $\operatorname{lcm}(18,24)$.','72','Take every prime at its largest required exponent.','Multiplying 18 and 24 without removing overlap.'),
('Convert $101101_2$ to base ten.','45','Expand as $32+8+4+1$.','Reading the numeral as decimal one hundred one thousand one hundred one.'),
('Write $47$ in base 2.','$101111_2$','Decompose 47 into powers of two.','Using decimal digits larger than 1.'),
('Find the units digit of $7^{23}$.','3','Use the period-four units-digit cycle of powers of 7.','Using 23 itself as the last digit.'),
('Find the least nonnegative residue of $-17$ modulo 6.','1','Add a multiple of 6 until the result lies from 0 through 5.','Reporting -5 without converting to the requested representative.'),
('Compute $38+57\pmod7$.','4','Reduce to $3+1$ modulo 7.','Adding first and forgetting to reduce.'),
('Is $123456$ divisible by 3?','Yes','Its digit sum is 21, which is divisible by 3.','Confusing the tests for 3 and 9.'),
('Correct the claim: Is $123456$ divisible by 9?','No','The digit sum is 21; 21 is not a multiple of 9.','Calling it divisible because 2+1 is 3.'),
('Find the remainder when $2^{20}$ is divided by 7.','4','Use $2^3\equiv1\pmod7$, so reduce exponent modulo 3.','Reducing 20 modulo 7 instead of the power cycle length.'),
('Find the number of positive divisors of $2^3 3^2 5$.','24','Choose exponents independently: $(3+1)(2+1)(1+1)$.','Adding exponents instead of adding one and multiplying.'),
('Find the greatest integer that divides both 252 and 198.','18','Use Euclid: 252-198=54, 198 mod 54=36, 54 mod 36=18.','Choosing 36 although it does not divide 198.'),
('Find the least positive integer divisible by 12, 15, and 18.','180','Use $2^2\cdot3^2\cdot5$.','Using the product 3240.'),
('Convert $2A_{16}$ to base ten.','42','Use $2\cdot16+10$.','Treating A as 1.'),
('Write $100$ in base 5.','$400_5$','Four groups of $25$ make 100.','Writing $100_5$, which equals 25.'),
('Find the remainder when $3^{100}$ is divided by 10.','1','The powers of 3 have units cycle 3,9,7,1.','Using the exponent modulo 10.'),
('Show that the sum of two odd integers is even.','Let $2a+1$ and $2b+1$; their sum is $2(a+b+1)$.','Represent each odd integer in defining form.','Saying two examples are a proof.'),
('Find the last two digits of $11^{20}$.','01','Since $11^2=121\equiv21$ and powers can be reduced modulo 100; or use binomial expansion.','Assuming the last two digits repeat with period 2 without checking.'),
('Find the remainder when $5^{37}+3^{37}$ is divided by 4.','0','Reduce $5\equiv1$ and $3\equiv-1$ modulo 4.','Reducing only one term.'),
('A number leaves remainder 2 on division by 5 and remainder 3 on division by 4. Give the smallest positive example.','7','Test the numbers $2,7,12,\ldots$ modulo 4.','Using 23 without checking minimality.'),
('Find the gcd and lcm of 72 and 120.','gcd 24, lcm 360','Factor both and use minimum/maximum exponents.','Using the gcd exponents for both values.'),
('How many trailing zeros does $50!$ have in base ten?','12','Count factors of 5: $\lfloor50/5\rfloor+\lfloor50/25\rfloor$.','Counting factors of 2 instead of limiting factors of 5.'),
('Prove that consecutive integers are coprime.','Any common divisor divides their difference, 1.','Apply the difference property of common divisors.','Claiming consecutive integers have no factors.'),
('Can $n^2$ leave remainder 2 when divided by 4?','No','Check residues 0,1,2,3 modulo 4 and square them.','Testing only even n.'),
('Find the remainder of $1+2+\cdots+100$ modulo 9.','1','Use $100\cdot101/2=5050$ and reduce modulo 9.','Dividing a congruence by 2 without noting 2 is invertible mod 9.'),
('What is the smallest base in which $234$ is a valid numeral?','5','Every digit must be smaller than the base.','Answering 4 because 4 is the largest digit.'),
('Find the base-ten value of $123_4$.','27','Compute $1\cdot16+2\cdot4+3$.','Compute $1+2+3$.'),
('Show that $n^3-n$ is divisible by 6 for every integer n.','Factor as $n(n-1)(n+1)$; three consecutive integers supply factors 2 and 3.','Use consecutive-integer divisibility.','Claiming every factor is divisible by 6.'),
('Find the units digit of $9^{999}$.','9','Odd powers of 9 end in 9.','Using the even-power result 1.'),
('If $a\equiv b\pmod m$, why may one add the same integer c to both sides?','Because $(a+c)-(b+c)=a-b$ remains divisible by m.','Use the definition of congruence.','Treating congruence as equality without a divisibility argument.'),
('Give a counterexample to the claim that $a\equiv b\pmod m$ permits cancellation by every nonzero factor.','$2\cdot1\equiv2\cdot3\pmod4$, but $1\not\equiv3\pmod4$.','Use a noninvertible factor modulo a composite modulus.','Choosing a factor that is invertible modulo m.'),
('Explain why a prime factorization is unique up to order.','The fundamental theorem of arithmetic states it; divisibility by a prime forces the same prime to appear in any factorization.','State the theorem and its consequence.','Claiming uniqueness because examples look unique.'),
('Find all possible last digits of a square in base ten.','0, 1, 4, 5, 6, 9','Square the ten possible final digits.','Listing 2, 3, 7, or 8.'),
('Find the remainder when $10^{50}-1$ is divided by 99.','0','Since $10^2\equiv1\pmod{99}$, an even power is 1.','Using $10\equiv1\pmod{99}$.'),
('A clock has 12 positions. What remainder interpretation explains moving 29 hours forward?','29 is congruent to 5 modulo 12, so move five positions.','Model positions by residues modulo 12.','Calling the remainder 17.'),
('Design a divisibility test for 11 using decimal digits.','Use alternating digit sum because $10\equiv-1\pmod{11}$.','Expand place value modulo 11.','Using ordinary digit sum, which tests 3 or 9.'),
('Why is modular arithmetic useful for a last-digit question?','All numbers with the same residue modulo 10 have the same units digit.','Connect base-ten last digit to remainder modulo 10.','Saying it makes numbers smaller without naming the preserved property.')
]
tiers=['foundational']*12+['multi-step']*16+['contest-transfer']*8+['proof-strategy']*4
assert len(Q)==40
items=[]
for i,(p,a,o,t) in enumerate(Q,1):
    items.append({'id':f'aops-v1-ch05-q{i:03d}','skillIds':['factor-integers-and-use-divisibility','use-modular-arithmetic'],'archetype':['factor','gcd-lcm','base','remainder','proof'][i%5],'difficulty':tiers[i-1],'questionType':'freeResponse','prompt':p,'answer':a,'solutionOutline':o,'commonTrap':t,'intendedUse':'quiz-test-bank'})
doc={'metadata':{'id':'aops-v1-ch05-using-integers-bank','title':'AoPS Volume 1 Chapter 5: Using the Integers Question Bank','chapter':5,'topicIds':['aops-integers-number-theory'],'sourcePageRange':'pdf 53-65; printed 39-51','originalAuthoring':True,'distribution':{'foundational':12,'multi-step':16,'contest-transfer':8,'proof-strategy':4}},'items':items}
Path('docs/assessment-reference/aops-volume-1/chapter-05-using-the-integers-question-bank.yaml').write_text(yaml.safe_dump(doc,sort_keys=False,allow_unicode=True),encoding='utf8')
