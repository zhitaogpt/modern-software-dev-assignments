# Root Makefile to manage weekly assignments

.PHONY: test-week%

# Usage: make test-week6
test-week%:
	@if [ -d "week$*" ]; then \
		echo "Testing week$*"; \
		if [ -f "week$*/Makefile" ]; then \
			$(MAKE) -C week$* test; \
		else \
			echo "No Makefile found in week$*, attempting default pytest..."; \
			cd week$* && export PYTHONPATH=$$PYTHONPATH:$$(pwd)/backend && pytest backend/tests; \
		fi \
	else \
		echo "Directory week$* does not exist."; \
		exit 1; \
	fi
