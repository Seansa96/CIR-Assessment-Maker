from pathlib import Path
import yaml

Q = [
('A quantity y varies directly with x. If y=18 when x=6, find y when x=10.','30'),
('A quantity y varies inversely with x. If y=12 when x=4, find y when x=8.','6'),
('Red and blue beads are in the ratio 3:5. If there are 32 beads, how many are red?','12'),
('On a 1:50,000 map, 3 cm represents what actual distance?','1.5 km'),
('A price rises from $80 to $100. What is the percent increase?','25%'),
('Five identical notebooks cost $17.50. What do three cost?','$10.50'),
('A recipe uses flour:sugar=2:3. How much sugar is needed for 20 cups of flour?','30 cups'),
('Similar triangles have scale factor 3 from small to large. A 12-unit side becomes what length?','36'),
('A car travels 150 miles in 3 hours at constant speed. Find its speed.','50 mph'),
('Convert 2.5 meters to centimeters.','250 cm'),
('If a:b=4:7 and b=35, find a.','20'),
('Solve 6/9=x/30.','20'),
('A $50 meal has 18% tax. Find the total.','$59'),
('After a 25% discount, a jacket costs $54. Find its original price.','$72'),
('Six workers finish a job in 10 days at equal rates. How many days for 15 workers?','4 days'),
('A map scale is 1 inch:8 miles. Two towns are 5.5 inches apart. Find the actual distance.','44 miles'),
('A solution is 30% acid. How much acid is in 250 mL?','75 mL'),
('A 12-ounce drink is 25% juice. How many ounces of pure juice must be added to make it 40% juice?','3 ounces'),
('A machine makes 180 parts in 12 minutes. At that rate, how many in 35 minutes?','525'),
('A photograph is enlarged from 4 by 6 inches to 10 inches wide. Find the new height.','15 inches'),
('A $120 item is discounted 20% and then taxed 10% on the discounted price. Find the final price.','$105.60'),
('A pump fills 3/8 of a tank in 15 minutes. At a constant rate, how long for the full tank?','40 minutes'),
('A 4-person team needs 18 days. If two equally productive people join from day 1, how many days are needed?','12 days'),
('A mixture has milk:water=7:3. How much water is in 45 liters?','13.5 liters'),
('A currency exchange charges 2% of the amount exchanged. How many euros are received when $500 converts at 0.90 euro per dollar after the fee?','441 euros'),
('A 5-foot person casts a 4-foot shadow. At the same moment a tree casts a 28-foot shadow. Find the tree height.','35 feet'),
('A store marks an item up 30% and later discounts the marked price 30%. Is the final price the original price?','No; it is 91% of the original.'),
('Three taps fill a pool in 6, 8, and 12 hours respectively. What fraction of the pool do they fill in one hour together?','3/8'),
('A classroom ratio of girls to boys is 5:4. After 6 girls leave, it is 7:6. Find the original class size.','162'),
('A 15% solution is mixed with a 45% solution to make 20 liters of 30% solution. How many liters of each are used?','10 L of each'),
('A runner increases speed from 8 to 10 km/h. By what percent does travel time for a fixed distance decrease?','20%'),
('A blueprint uses 1 cm for 2.4 m. A room measures 7.5 cm on the blueprint. Find the actual length.','18 m'),
('The ratios p:q=2:3 and q:r=4:5. Find p:q:r in whole-number form.','8:12:15'),
('A recipe for 8 servings uses 1.5 cups of rice. You have 4.875 cups. What is the greatest whole number of servings possible?','26'),
('Why does cross multiplication in a/b=c/d require b and d to be nonzero?','The original fractions are undefined otherwise.'),
('Give a counterexample showing that a constant difference does not prove direct variation.','For example y=x+1 has constant difference but y/x is not constant.'),
('Choose a model: does the time to transfer a fixed file vary directly or inversely with download speed?','Inversely'),
('Explain why successive 20% increase and 20% decrease do not cancel.','They use different bases; factor 1.2 times 0.8 is 0.96.'),
('Two similar rectangles have side ratio 2:5. What is their area ratio, and why?','4:25; area scales by the square of the length factor.'),
('A recipe is doubled and then made 25% smaller than that doubled batch. What multiple of the original batch remains?','1.5 times the original')
]

OUTLINES = [
'Find k=18/6 and compute 3(10).', 'Keep xy constant: 12(4)=y(8).', 'There are 8 total ratio parts; take 3/8 of 32.', 'Multiply 3 cm by 50,000 and convert centimeters to kilometers.',
'Divide the change 20 by the original 80.', 'Find one notebook price, then multiply by 3.', 'Scale both recipe parts by 20/2.', 'Multiply the small side by the linear scale factor.',
'Use rate=distance/time.', 'Use 100 centimeters per meter.', 'The scale factor from 7 to 35 is 5; multiply 4 by 5.', 'Cross multiply 6(30)=9x.',
'Compute 50(1.18).', 'The sale price is 75% of original: 54/.75.', 'Fixed work means workers times days is constant.', 'Multiply the map length by 8 miles per inch.',
'Take 30% of 250.', 'Let x be added juice and solve (3+x)/(12+x)=.4.', 'Find 15 parts per minute then multiply by 35.', 'The width scale is 10/4; apply it to 6.',
'Apply the discount first, then tax the reduced amount.', 'If 3/8 needs 15 minutes, one whole needs 8/3 as long.', 'Work is 72 person-days, so divide by 6 people.', 'Take 3/10 of 45 liters.',
'The fee leaves .98(500); exchange the remainder at .90.', 'Equal sun angle gives height/shadow=5/4.', 'Compare factors 1.30 and .70.', 'Add hourly rates 1/6+1/8+1/12.',
'Let girls=5k and boys=4k; solve (5k-6)/(4k)=7/6.', 'Let x be liters of 15%; the other amount is 20-x.', 'For fixed distance time is inverse to speed; compare 8/10.', 'Multiply 7.5 by 2.4.',
'Match q using LCM 12 before combining ratios.', 'Find servings per cup, then take the largest integer not exceeding the result.', 'State the domain restriction before multiplying.', 'Compare y/x, not y-x, for direct variation.',
'For fixed file size, time=filesize/speed.', 'Compute the two multiplicative factors.', 'Square the linear ratio 2:5.', 'Compute 2 times .75.'
]
TRAPS = [
'Adding 4 instead of scaling.', 'Using 12/4=8/y incorrectly.', 'Using 3/5 of the total.', 'Stopping at 150,000 cm without converting units.',
'Dividing by the new price.', 'Multiplying the five-book price by 3.', 'Reversing flour and sugar.', 'Scaling area instead of a side.',
'Using 150 times 3.', 'Treating 2.5 as 25 cm.', 'Scaling both terms by different factors.', 'Cross multiplying 6x=9(30).',
'Adding 18 dollars rather than 18 percent.', 'Subtracting 25% of 54.', 'Treating workers and days as direct variation.', 'Dividing by 8 rather than multiplying.',
'Taking 30% as 0.03.', 'Adding 3 ounces without solving for the new total.', 'Dividing 180 by 35.', 'Using an area scale factor.',
'Taxing the original price.', 'Assuming 15 minutes per eighth.', 'Adding workers and days.', 'Taking 7/10 of the water.',
'Charging the fee after conversion without saying so.', 'Comparing heights without shadows.', 'Subtracting 30%-30%=0.', 'Adding times rather than rates.',
'Changing only one ratio part after six leave.', 'Averaging 15% and 45% without amounts.', 'Saying time decreases 25%.', 'Reversing the blueprint scale.',
'Combining ratios without matching q.', 'Rounding up beyond available rice.', 'Cancelling denominators that could be zero.', 'Mistaking a linear pattern for proportionality.',
'Calling it direct because speed increases.', 'Subtracting percentages instead of multiplying factors.', 'Using 2:5 for area.', 'Treating 25% smaller as subtracting .25 from the original after doubling.'
]

tiers = ['foundational'] * 12 + ['multi-step'] * 16 + ['contest-transfer'] * 8 + ['proof-strategy'] * 4
assert len(Q) == len(OUTLINES) == len(TRAPS) == len(tiers) == 40
items=[]
for i, ((prompt, answer), outline, trap, difficulty) in enumerate(zip(Q, OUTLINES, TRAPS, tiers), 1):
    items.append({'id': f'aops-v1-ch04-q{i:03d}', 'skillIds': ['apply-proportions', 'check-proportions-restrictions'], 'archetype': ['direct', 'inverse', 'ratio', 'scale', 'percent', 'rate', 'mixture', 'strategy'][i % 8], 'difficulty': difficulty, 'questionType': 'freeResponse', 'prompt': prompt, 'answer': answer, 'solutionOutline': outline, 'commonTrap': trap, 'intendedUse': 'quiz-test-bank'})
doc={'metadata': {'id': 'aops-v1-ch04-proportions-bank', 'title': 'AoPS Volume 1 Chapter 4: Proportions Question Bank', 'chapter': 4, 'topicIds': ['aops-proportions'], 'sourcePageRange': 'pdf 42-52; printed 28-38', 'originalAuthoring': True, 'distribution': {'foundational': 12, 'multi-step': 16, 'contest-transfer': 8, 'proof-strategy': 4}}, 'items': items}
Path('docs/assessment-reference/aops-volume-1/chapter-04-proportions-question-bank.yaml').write_text(yaml.safe_dump(doc, sort_keys=False, allow_unicode=True), encoding='utf8')
