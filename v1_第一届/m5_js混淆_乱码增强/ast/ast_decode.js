const {parse} = require("@babel/parser")
const traverse = require("@babel/traverse").default;
const generator = require("@babel/generator").default
const types = require("@babel/types")

var fs = require("fs");

var code = fs.readFileSync("ast_source.js",{encoding:"utf-8"});
let ast_parse = parse(code)


// 获取解密函数 并且写入内存
let member_decode_js = "";

for (let i=0;i<=2;i++){
    member_decode_js+= generator(ast_parse.program.body[i],{compact:true}).code
}
eval(member_decode_js)
console.log(c("fAq6", 1064))
