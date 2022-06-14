livehtml:
	$(MAKE) -C docs livehtml

html:
	$(MAKE) -C docs html

install:
	python3 -m pip install --user .[docs,dev]

build:
	python3 -m build

test:
	rm -f .coverage coverage.xml
	pytest hepi

commit: 
	-git add .
	-git commit

push: commit
	git push

pull: commit
	git pull

clean: 
	rm -r .eggs .pytest_cache hepi.egg-info dist build


release: push html
	git tag $(shell git describe --tags --abbrev=0 | perl -lpe 'BEGIN { sub inc { my ($$num) = @_; ++$$num } } s/(\d+\.\d+\.)(\d+)/$$1 . (inc($$2))/eg')
	git push --tags
