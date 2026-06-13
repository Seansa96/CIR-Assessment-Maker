# planned-features.md

# Planned Features

This document tracks intended features beyond the first working MVP.

## MVP Features

The first working version should include:

* ASP.NET Core backend
* Astro frontend
* Localhost development
* File-backed data storage
* YAML/JSON assessment loading
* Category browsing
* Subcategory support
* Quiz/test loading
* Practice mode
* Scored mode
* Multiple choice questions
* Select-all questions
* Free response self-check questions
* Attempt recording
* Grade log committing
* Settings page
* Assessment validation
* Sample STEM assessments

## Near-Term Features

### Assessment Creation

Add a creation flow where the user can:

* Create quiz
* Create test
* Select category
* Select subcategory
* Choose default template
* Create custom assessment
* Add/remove questions
* Change question type on the fly
* Preview assessment before saving
* Validate before save

### Question Authoring Improvements

Support a more user-friendly question creation workflow:

* Form-based multiple choice editor
* Select-all editor
* Free response editor
* Explanation editor
* Answer bank validation
* Duplicate ID detection
* Auto-generated question IDs
* YAML/JSON preview panel

### Matching Questions

Add matching question support.

Required behavior:

* Left/right pair definition
* Shuffled answer order
* Correct pair validation
* Explanation support
* Scoring support

### Grade Analytics

Improve grade tracking:

* Category-level grades
* Subcategory-level grades
* Weighted subcategories
* Quiz/test weighting
* Practice vs scored attempt filtering
* Attempt history
* Weak-topic summaries

## Medium-Term Features

### Automatic Test Creation

Allow the user to generate a test from existing quizzes.

Initial constraints:

* Single category only
* Select multiple quizzes
* Choose total question count
* Pull as evenly as possible from selected subcategories
* Randomize by default
* Allow generated test to be taken immediately
* Optionally save generated test as a new assessment

Future version:

* Multi-category test generation
* Difficulty balancing
* Question type balancing
* Weak-topic weighting

### Timers

Support:

* Assessment-level timers
* Question-level timers
* Timed and untimed modes
* Per-assessment overrides
* Per-question overrides
* Timer pause behavior setting
* Timer expiration behavior setting

Default:

* Untimed assessment
* Untimed questions

### Advanced Question Types

Potential additions:

* Numeric answer with tolerance
* Ordering questions
* Fill-in-the-blank
* Equation entry
* Multi-part questions
* Proof/rubric-based questions
* Diagram/image-based questions
* Code-output questions
* Debugging questions

## Long-Term Features

### Database Support

Add SQLite support while preserving repository interfaces.

Possible migration targets:

* Settings
* Categories
* Assessments
* Attempts
* Grade logs
* Tags
* Templates

### Rich Study System Integration

Integrate with Cognitive Inquiry and Remediation notes.

Possible features:

* Attach CIR score to subcategory
* Recommend remediation based on score band
* Track friction type
* Track failure modes
* Link assessment results to remediation protocols
* Generate weak-topic review queue

### Import / Export

Support:

* Export assessment to YAML
* Export attempt history
* Export grade log
* Import assessment packs
* Validate imported packs

### UI Improvements

* Better dashboard
* Category cards
* Subcategory progress display
* Result graphs
* Attempt review pages
* Settings editor improvements
* Dark mode
* Keyboard navigation
* Mobile-friendly layout
* Replace code question textareas with CodeMirror 6 for indentation, syntax highlighting, bracket matching, and language-aware editing

## Deferred Features

These are intentionally not part of the MVP:

* Authentication
* Cloud sync
* Multi-user classrooms
* Public deployment
* AI grading
* Collaborative assessment creation
* Payment features
* Mature permission handling
* LMS integrations
