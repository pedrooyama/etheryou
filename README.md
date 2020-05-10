# Etheryou

We provide three ways of running EtherYou:

* [Running with Docker with Linux startup script](#running-with-docker-with-linux-startup-script)

* [Running with Docker from terminal (Linux/Windows)](#running-with-docker-from-terminal-linuxwindows)

* [Running from Linux terminal](#running-from-linux-terminal)

## Running with Docker with Linux startup script:
1.  Clone docker project:
	```console
	git clone https://github.com/pedrooyama/etheryou-docker.git
	cd etheryou-docker
	```

1.  Run blockchain container:
	```console
	./run-etheryou-blockchain.sh
	```
	and wait for the message **BLOCKCHAIN READY!**

1.  Run client container (in a new terminal):
	```console
	./run-etheryou-client.sh
	```
	and follow instructions.

## Running with Docker from terminal (Linux/Windows):

1.  Run blockchain container:
	```console
	docker run --rm -it --name etheryou-blockchain oyamapedro/etheryou-blockchain
	```

1.  Run client container (in a new terminal):
	* To run the client software:
	```console
	docker run  --link etheryou-blockchain --rm -it oyamapedro/etheryou-client main/run.py
	```

	* To run 'Gas x Message Length' experiment:
	```console
	docker run -v /path/to/results/directory:/src/app/reports/ --link etheryou-blockchain --rm -it oyamapedro/etheryou-client experiments/gas_x_message_length.py /src/app/reports/
	```

	* To run 'Gas x Number of Recipients' experiment:
	```console
	docker run -v /path/to/results/directory:/src/app/reports/ --link etheryou-blockchain --rm -it oyamapedro/etheryou-client experiments/gas_x_number_of_recipients.py /src/app/reports/
	```

## Running from Linux terminal:
1.  Deploy the smart contract
	Download the contract ([EtherYou.sol](https://raw.githubusercontent.com/pedrooyama/etheryou/master/smart_contract/EtherYou.sol "EtherYou.sol")) and deploy it using [Ganache Truffle](https://www.trufflesuite.com/ganache "Ganache Truffle").

1.  Clone the project
	```console
	git clone https://github.com/pedrooyama/etheryou.git
	cd etheryou
	```
1.  Install dependencies
	```console
	pip install -r requirements.txt
	```

1.  Config
	1. Edit `parameters/config.py`:
	Set `rpc_server`, where the contract is deployed. Ex: 'http://localhost:8545'.
	Set `truffle_file_path`, the path to the Truffle EtherYou.json file.
	Set `contract_address`.
	Set `experiments_output_directory`, the directory the experiments scripts save their results.

	1. Edit `repository/user_repository.py`:
	Set Ethereum Key Pair `eth_public_key_A ` and  `eth_private_key_A`. 
	The Ethereum Key Pair `eth_public_key_B ` and  `eth_private_key_B` is only necessary to run `test test/test_message_block.py`.

1.  Set PYTHONPATH:
	```console
	export set PYTHONPATH=.
	```

1.  Execute a script:
	* To run the client software:
	```console
	python main/run.py
	```
	* To run 'Gas x Message Length' experiment:
	```console
	python experiments/gas_x_message_length.py
	```

	* To run 'Gas x Number of Recipients' experiment:
	```console
	python experiments/gas_x_number_of_recipients.py
	```
