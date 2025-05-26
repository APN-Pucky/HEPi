livehtml:
	hatch run docs:$(MAKE) -C docs livehtml

html:
	hatch run docs:$(MAKE) -C docs html

doc: html
docs: html

install:
	lhapdf install cteq6l1 cteq66 CT14lo CT14nlo
	python3 -m pip install -user .

install-user:
	python3 -m pip install --user --break-system-packages .

build:
	hatch build

test:
	rm -f .coverage coverage.xml
	hatch run test:pytest

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
