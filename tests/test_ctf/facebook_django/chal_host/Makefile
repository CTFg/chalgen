build:
	docker build . -t chal_host-8778991352829

run: build
	docker run  chal_host-8778991352829

clean:
	docker rm -f -v chal_host-8778991352829

generate-img:
	docker run -d --name chal_host-8778991352829 chal_host-8778991352829:latest
	docker export chal_host-8778991352829 -o vm.tar.gz
	docker stop chal_host-8778991352829