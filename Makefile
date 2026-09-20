.PHONY: verify safe clean help

help:
	@echo "make verify  - run every check (safety, shape, citations, derivations, judgement, self-test, history)"
	@echo "make safe    - run the public-safety scan alone, before publishing"

verify:
	@python3 _verify/scan_public_safety.py
	@python3 _verify/verify_shape.py
	@python3 _verify/verify_citations.py
	@python3 _verify/spanish_numbers.py > /dev/null && echo "ok    parser       spanish number and date parser self-test passes"
	@python3 _verify/verify_derivations.py
	@python3 _verify/verify_no_judgement.py
	@python3 _verify/test_verifiers.py
	@python3 _verify/test_history_scan.py

safe:
	@python3 _verify/scan_public_safety.py
