from pathlib import Path
import yaml

Q = [
("Evaluate $2^0+5^{-1}$.","6/5","Use the zero and negative exponent definitions.","Reading a negative exponent as a negative value."),
("Write $1/(3^4)$ as a power of 3.","3^{-4}","A reciprocal reverses the exponent sign.","Writing $-3^4$."),
("Simplify $(x^7)(x^{-3})$.","x^4","Combine exponents only for the same base.","Subtracting because one exponent is negative."),
("Simplify $a^{12}/a^5$ for $a\\ne0$.","a^7","Cancel seven common factors.","Dividing exponents."),
("Evaluate $16^{3/4}$.","8","Take the fourth root, then cube.","Using $16^{3}/4$."),
("Simplify $\sqrt{72}$.","6\\sqrt2","Extract the largest square factor.","Replacing it with $\\sqrt{36}+\\sqrt2$."),
("State $\sqrt{x^2}$ for real $x$.","|x|","The principal square root is nonnegative.","Answering $x$ for negative x."),
("Rationalize $5/\sqrt3$.","5\\sqrt3/3","Multiply top and bottom by $\\sqrt3$.","Multiplying only the denominator."),
("Find $\log_2 32$.","5","Ask which exponent on 2 gives 32.","Dividing 32 by 2 once."),
("Find $\log_{10}(0.01)$.","-2","$10^{-2}=0.01$.","Ignoring negative logarithms."),
("For which real x is $\log_4(x-7)$ defined?","x>7","A real logarithm needs a positive argument.","Allowing $x=7$."),
("Solve $3^{x+1}=81$.","x=3","Rewrite 81 as $3^4$.","Taking $x=4$."),
("Simplify $(2x^3y^{-2})^2$ using positive exponents.","4x^6/y^4","Apply the power to each factor.","Leaving $y^{-4}$ when positive form is requested."),
("Simplify $(a^2b^3)^4/(a^3b)$.","a^5b^{11}","Multiply exponents inside, then subtract across division.","Adding exponents in the quotient."),
("Evaluate $27^{-2/3}$.","1/9","Cube root first: $27^{1/3}=3$.","Making the answer $-9$."),
("Simplify $\sqrt[3]{54}$.","3\\sqrt[3]2","Extract $27$ as a cube factor.","Using a square-factor rule."),
("Rationalize $1/(2-\sqrt3)$.","2+\\sqrt3","Use the conjugate; denominator becomes 1.","Multiplying by $2-\\sqrt3$ again."),
("Solve $5^{2x}=125$.","x=3/2","Rewrite 125 as $5^3$.","Answering 3."),
("Solve $\log_3 x=4$.","x=81","Convert the logarithm to exponential form.","Using $x=12$."),
("Solve $\log_2(x+1)=3$.","x=7","Exponentiate then check the argument.","Keeping $x=8$."),
("Solve $\log_5(x-1)+\log_5(x+1)=1$.","x=\\sqrt6","Combine logs, solve, and retain $x>1$.","Keeping the negative square root."),
("Solve $\sqrt{x+5}=x-1$.","x=4","Require $x\\ge1$, square, then verify.","Keeping the extraneous root -1."),
("Compare $8^{11}$ and $4^{17}$.","8^{11}>4^{17}","Rewrite as powers of 2: $2^{33}$ and $2^{34}$? Correct comparison is $4^{17}>8^{11}$.","Comparing bases without common exponents."),
("Correct the previous comparison: which is larger, $8^{11}$ or $4^{17}$?","4^{17}","Use $8^{11}=2^{33}$ and $4^{17}=2^{34}$.","Repeating an unchecked conclusion."),
("Simplify $(9x^4)^{1/2}$ when $x\\ge0$.","3x^2","Use the stated sign condition.","Writing $3x$."),
("If $2^a=7$ and $2^b=5$, express $2^{a-b}$.","7/5","Use the quotient law before substituting.","Using $7-5$."),
("Find all real x satisfying $x^{2/3}=4$.","x=8,-8","Cube first or set $\\sqrt[3]x=\\pm2$.","Giving only 8."),
("Simplify $\frac{\sqrt{x^5}}{\sqrt{x}}$ for $x>0$.","x^2","Combine radicals under the positive-domain condition.","Answering $x^4$."),
("Solve $4^x=7$ exactly.","x=\\log_4 7","A logarithm names the needed exponent.","Claiming no solution because 7 is not a power of 4."),
("Explain why $\log_2(-8)$ has no real value.","No real exponent on positive 2 gives a negative result.","Use the range of a positive-base exponential function.","Treating logs as roots."),
("Prove $a^m a^n=a^{m+n}$ for positive integers.","Both sides are m+n copies of a.","Count repeated factors.","Citing the rule as its own proof."),
("Prove $a^{-n}=1/a^n$ for $a\\ne0$.","From $a^n a^{-n}=a^0=1$.","Use the inverse needed for product 1.","Assuming the result for a=0."),
("A student says $\sqrt{a+b}=\sqrt a+\sqrt b$. Give a counterexample.","a=b=1: $\\sqrt2\\ne2$.","Test a small positive pair.","Using a=0, which does not disprove it."),
("Why must $\log_b x$ require $b\\ne1$?","Base 1 never produces values other than 1.","An inverse needs a one-to-one exponential function.","Saying only that it is a convention."),
("Choose a method for $9^{x}=27^{x-1}$.","Rewrite both bases as powers of 3.","Common-base rewriting makes exponents comparable.","Taking decimal approximations first."),
("Choose a method for $\sqrt{50}-\sqrt8$.","Extract square factors then combine like radicals.","Both radicals reduce to multiples of $\\sqrt2$.","Subtracting inside one radical."),
("A formula contains $\log(x-2)$ after squaring an equation. What check is mandatory?","Verify $x>2$ and test the original equation.","Domain and extraneous-root checks are separate.","Checking only the squared equation."),
("Design a one-line verification for $\log_3 81=4$.","Show $3^4=81$.","Use the inverse definition.","Recomputing an unrelated decimal."),
("Explain why rationalizing $1/(\sqrt5+\sqrt2)$ uses a conjugate.","The conjugate product removes the cross radicals and is rational.","Use $(u+v)(u-v)=u^2-v^2$.","Multiplying by an arbitrary radical."),
("A solution divides by $x-3$. What case must be checked separately?","x=3","The divisor could be zero and discard a case.","Only check x=0."),
]
tiers = ["foundational"]*12 + ["multi-step"]*16 + ["contest-transfer"]*8 + ["proof-strategy"]*4
items=[]
for i,(p,a,o,t) in enumerate(Q,1):
    items.append({"id":f"aops-v1-ch01-q{i:03d}","skillIds":["apply-exponents-and-logarithms","check-exponents-and-logarithms-restrictions"],"archetype":["recognition","direct-application","condition-check","changed-condition","synthesis"][i%5],"difficulty":tiers[i-1],"questionType":"freeResponse","prompt":p,"answer":a,"solutionOutline":o,"commonTrap":t,"intendedUse":"quiz-test-bank"})
doc={"metadata":{"id":"aops-v1-ch01-exponents-and-logarithms-bank","title":"AoPS Volume 1 Chapter 1: Exponents and Logarithms Question Bank","chapter":1,"topicIds":["aops-exponents-logarithms"],"sourcePageRange":"pdf 15-26; printed 1-12","originalAuthoring":True,"distribution":{"foundational":12,"multi-step":16,"contest-transfer":8,"proof-strategy":4}},"items":items}
Path("docs/assessment-reference/aops-volume-1/chapter-01-exponents-and-logarithms-question-bank.yaml").write_text(yaml.safe_dump(doc,sort_keys=False,allow_unicode=True),encoding="utf-8")
