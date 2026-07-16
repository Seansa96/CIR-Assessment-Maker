from pathlib import Path
import yaml

# Hand-authored prompts; no parameterized prompt generation.
Q=[
("Evaluate $i^{37}$.","i"),("Write $(3+4i)+(5-9i)$ in standard form.","8-5i"),("Compute $(6-2i)-(1+7i)$.","5-9i"),("Find the real part of $-8+3i$.","-8"),("Find $i^2+i^3+i^4$.","-1-i"),("Simplify $\sqrt{-49}$.","7i"),("Compute $(2+i)(2-i)$.","5"),("Which is larger: $|3+4i|$ or $|1+5i|$?","|1+5i|"),("Solve $z+ (4-3i)=10+i$.","z=6+4i"),("Write $7i+(-2)$ in standard form.","-2+7i"),("Compute $(1+i)^2$.","2i"),("Compute $(3-2i)(4+i)$.","14-5i"),("Simplify $(5+i)/(5-i)$.","(12+5i)/13"),("Find $i^{2026}$.","-1"),("If $a+bi=7-2i$, find $a-b$.","9"),("Solve $(x+2i)(x-2i)=13$ for real x.","x=+-3"),("Find the conjugate of $-6+11i$.","-6-11i"),("Compute $(2-3i)^2$.","-5-12i"),("Simplify $i(4-7i)$.","7+4i"),("Find all real x for which $x^2+9=0$ has a real solution.","none"),("Solve $z^2=-16$.","z=4i,-4i"),("Compute $(1-i)^3$.","-2-2i"),("Show whether $3+2i=3-2i$.","false"),("Divide $8+6i$ by $2-i$.","2+4i"),("Find the imaginary part of $(3+i)(3-i)$.","0"),("Simplify $\sqrt{-12}$.","2i\\sqrt3"),("Compute $(4+i)(4-i)(2+i)$.","34+17i"),("If $z=1+i$, find $z^4$.","-4"),("Solve $z+(\bar z)=10$ when $z=5+bi$.","any real b"),("Explain why $a+bi=0$ implies $a=b=0$.","uniqueness of standard form"),("Prove $i^{n+4}=i^n$.","because i^4=1"),("Give a counterexample to $\sqrt{ab}=\sqrt a\sqrt b$ over complex numbers using a=b=-1.","left 1, right -1"),("Choose the quickest method for $i^{12345}$.","reduce exponent modulo four"),("Explain why multiplying by a conjugate helps divide complex numbers.","denominator becomes a real sum of squares"),("A student says $(a+bi)^2=a^2+b^2i$. Name the missing term.","2abi and sign change from i^2"),("Find a complex number whose square is $8i$.","2+2i or -2-2i"),("Show that $(a+bi)(a-bi)$ is real.","cross terms cancel; result a^2+b^2"),("When can a complex quotient have denominator zero?","when both real and imaginary denominator parts are zero"),("Explain why a real-number equation can gain solutions after extending to complex numbers.","negative values may have complex square roots"),("Design a verification for a proposed quotient z=w/v.","multiply proposed z by v and compare with w")]
Q[4] = (Q[4][0], '-i')
tiers=['foundational']*12+['multi-step']*16+['contest-transfer']*8+['proof-strategy']*4
items=[]
for i,(p,a) in enumerate(Q,1):
 outlines=[
  'Use the period-four power cycle.', 'Add real and imaginary components.', 'Distribute the subtraction.', 'Read the real coefficient.',
  'List the three powers of i and add.', 'Factor out sqrt(-1).', 'Use conjugate factors.', 'Compare squared moduli.',
  'Subtract the known addend.', 'Write real plus imaginary form.', 'Expand and use i squared.', 'FOIL before collecting terms.',
  'Rationalize with the conjugate.', 'Reduce the exponent modulo four.', 'Match standard-form coefficients.', 'Use the difference of squares.',
  'Change only the imaginary sign.', 'Expand the binomial completely.', 'Distribute i, then simplify.', 'Use the fact that real squares are nonnegative.',
  'Take both complex square roots.', 'Square then multiply once.', 'Compare real and imaginary parts.', 'Multiply by the conjugate of 2-i.',
  'Use the conjugate product.', 'Separate 12 into 4 times 3.', 'Collapse the first conjugate pair.', 'Square z twice.',
  'Add z to its conjugate.', 'Invoke uniqueness of a+bi form.', 'Factor out i to the fourth.', 'Compare principal square roots.',
  'Reduce the exponent rather than expanding.', 'Make the denominator a real norm.', 'Expand to expose 2abi and i squared.', 'Compare components after squaring.',
  'Show the cross terms cancel.', 'Set both components of the denominator to zero.', 'Contrast real square roots with complex ones.', 'Multiply the proposed quotient by the divisor.'
 ]
 traps=[
  'Ignoring the power cycle.', 'Combining unlike components.', 'Losing a minus sign.', 'Naming the imaginary part.',
  'Using i to the fourth as -1.', 'Writing -7i.', 'Forgetting cancellation.', 'Comparing coordinates instead of moduli.',
  'Changing both signs.', 'Putting i first.', 'Treating i squared as 1.', 'Dropping an i squared term.',
  'Not rationalizing the denominator.', 'Using period two.', 'Adding a and b.', 'Expanding x plus 2i incorrectly.',
  'Negating the real part too.', 'Using a squared plus b squared as the real part.', 'Leaving i squared unchanged.', 'Accepting an imaginary real-number solution.',
  'Giving only one root.', 'Stopping after the square.', 'Assuming conjugates are equal.', 'Multiplying by the denominator again.',
  'Calling a real product imaginary.', 'Leaving sqrt(12) unsimplified.', 'Multiplying all three first.', 'Using the modulus instead.',
  'Forcing b to zero.', 'Allowing cancellation of components.', 'Using i fourth equals -1.', 'Ignoring the principal-root convention.',
  'Repeated multiplication.', 'Changing only the numerator.', 'Omitting the sign from i squared.', 'Giving a number whose square is -8i.',
  'Keeping cross terms.', 'Allowing one nonzero component.', 'Claiming all equations gain roots.', 'Checking against the wrong product.'
 ]
 items.append({'id':f'aops-v1-ch02-q{i:03d}','skillIds':['apply-complex-numbers','verify-complex-numbers-solutions'],'archetype':['standard-form','power-cycle','conjugate','equation','proof'][i%5],'difficulty':tiers[i-1],'questionType':'freeResponse','prompt':p,'answer':a,'solutionOutline':outlines[i-1],'commonTrap':traps[i-1],'intendedUse':'quiz-test-bank'})
doc={'metadata':{'id':'aops-v1-ch02-complex-numbers-bank','title':'AoPS Volume 1 Chapter 2: Complex Numbers Question Bank','chapter':2,'topicIds':['aops-complex-numbers'],'sourcePageRange':'pdf 27-30; printed 13-16','originalAuthoring':True,'distribution':{'foundational':12,'multi-step':16,'contest-transfer':8,'proof-strategy':4}},'items':items}
Path('docs/assessment-reference/aops-volume-1/chapter-02-complex-numbers-question-bank.yaml').write_text(yaml.safe_dump(doc,sort_keys=False,allow_unicode=True),encoding='utf8')
