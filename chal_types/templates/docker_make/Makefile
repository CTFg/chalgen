build:
	@docker build . -t {chal_name} -q

run: build
	@docker run {chal_run_options} {chal_name}

clean:
	@docker rm -f -v {chal_name}

generate-img:
	@docker run -d --name {chal_name} {chal_name}:latest
	@docker export {chal_name} -o vm.tar.gz
	@docker rm {chal_name}
	@docker rmi {chal_name}