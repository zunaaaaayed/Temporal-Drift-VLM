.PHONY: setup check smoke research
setup:
	bash scripts/bootstrap.sh core
check:
	bash scripts/checks.sh
smoke:
	.venv/bin/tdrift smoke
research:
	.venv/bin/tdrift run --config configs/research.json --with-style --stages plots grids projections
