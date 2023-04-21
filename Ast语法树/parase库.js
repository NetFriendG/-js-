const parse = require('@babel/core')
const traverse = require('@babel/traverse').default
const generator = require('@babel/generator').default
const fs = require('fs')

// js_code = `var a = "\u0068\u0065\u006c\u006c\u006f\u002c\u0041\u0053\u0054"`
js_code  = fs.readFileSync('xl.js',{encoding:"utf-8"})

let ast = parse.parse(js_code)
//
// const vistor = {
//     VariableDeclaration(path) {
//         // path.node  获取当前路径的node节点
//         // console.log(path.toString()); 获取源代码
//         //console.log(path.type) //VariableDeclaration  获取当前节点类型
//         console.log(path.parent);
//     }
// }

vistor1 = {
    StringLiteral(path){
        path.node.extra.raw = path.node.rawValue;

    }
}


// traverse(ast,vistor1)
//
let {code} = generator(ast)

fs.writeFile('decode.js',code,(err)=>{})




