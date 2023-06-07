const wasm2js = require('wasm2js')
const fs = require('fs')

const wasmBuffer = fs.readFileSync('main.wasm')
const js = wasm2js(wasmBuffer)
console.log(js)

function m() {
    t1 = parseInt(Date.parse(new Date()) / 1000 / 2);
    t2 = parseInt(Date.parse(new Date()) / 1000 / 2 - Math.floor(Math.random() * (50) + 1));
    return window.q(t1, t2).toString() + '|' + t1 + '|' + t2;
}