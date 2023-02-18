const {ethers} = require('ethers');
require('dotenv').config()
console.log(process.env.privateKey)
const RPC = process.env.RPC; // RPC url here
const account1 = process.env.account1; // public address here
const privateKey = process.env.privateKey; // private key here

const provider = new ethers.providers.JsonRpcProvider(
    RPC
)

const wallet = new ethers.Wallet(privateKey, provider);


async function call() {
    const bal = await provider.getBalance(account1);
    console.log(account1, ":" ,ethers.utils.formatEther(bal));
    console.log(await wallet.getAddress(), ":" ,ethers.utils.formatEther(await wallet.getBalance()));
    
    const trans = await wallet.sendTransaction({
        to: process.env.to,
        value: ethers.utils.parseEther('0.0001')
    })
    
    await trans.wait();
    
    const bal2 = await provider.getBalance(account1);
    console.log(account1, ":" ,ethers.utils.formatEther(bal2));
    console.log(await wallet.getAddress(), ":" ,ethers.utils.formatEther(await wallet.getBalance()));
    
    console.log(trans)

}

call()