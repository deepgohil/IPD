import os
import boto3
from dotenv import load_dotenv
from web3 import Web3
from dotenv import dotenv_values
from typing import Union
from fastapi import FastAPI
# ////////////////////////////////SET ENV
config = dotenv_values(".env")
infura_url = config['RPC']
private_key = config['privateKey']
from_account = config['account1']
to_account = config['to']

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/trans")
def startTrans():
      web3 = Web3(Web3.HTTPProvider(infura_url))
      nonce = web3.eth.getTransactionCount(from_account)

      tx = {
          'type': '0x2',
          'nonce': nonce,
          'from': from_account,
          'to': to_account,
          'value': web3.toWei(0.001, 'ether'),
          'maxFeePerGas': web3.toWei('100', 'gwei'),
          'maxPriorityFeePerGas': web3.toWei('2', 'gwei'),
          'chainId': 5
      }

      gas = web3.eth.estimateGas(tx)
      tx['gas'] = gas
      signed_tx = web3.eth.account.sign_transaction(tx, private_key)
      tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
      recpt=web3.eth.wait_for_transaction_receipt(tx_hash)
      print(signed_tx)
      print(recpt)
      print(tx_hash)

      dataMsg=str(recpt)
      for i in range(5):
            client = boto3.client(
            "sns",
            aws_access_key_id=config['aws_access_key_id'],
            aws_secret_access_key=config['aws_secret_access_key'],
            region_name="ap-south-1"
          )

            client.publish(
              PhoneNumber="+918104680835",
              Message="YOUR TRANSECTION IS SUCESSFULL"
            )
      return {"Hash": str(web3.toHex(tx_hash))}      