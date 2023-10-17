livehtml:
	poetry run $(MAKE) -C docs livehtml

html:
	poetry run $(MAKE) -C docs html

doc: html

install:
	lhapdf install cteq6l1 cteq66 CT14lo CT14nlo
	poetry install --with docs --with test
	# Make lhapdf available in the virtualenv
	sed -i 's/include-system-site-packages\s*=.*/include-system-site-packages = true/g' $(shell poetry env info -p)/pyvenv.cfg

install-user:
	python3 -m pip install --user --break-system-packages .

build:
	poetry build

test:
	rm -f .coverage coverage.xml
	poetry run pytest

commit: 
	-git add .
	-git commit

push: commit
	git push

pull: commit
	git pull

clean: 
	rm -r .eggs .pytest_cache *.egg-info dist build


release: push html
	git tag $(shell git describe --tags --abbrev=0 | perl -lpe 'BEGIN { sub inc { my ($$num) = @_; ++$$num } } s/(\d+\.\d+\.)(\d+)/$$1 . (inc($$2))/eg')
	git push --tags
