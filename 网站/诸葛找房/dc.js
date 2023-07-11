const parse = require('@babel/parser')
const traverse = require('@babel/traverse').default
const generator = require('@babel/generator').default
const types = reqire('@bable/types');
const fs = require('fs')

process.argv.length > 2 ? File1 = process.argv[2] : File1 = './encode.js'
process.argv.length > 3 ? File2 = process.argv[2] : File2 = './decode.js'
let js_code = fs.readFileSync(File1, {encoding: "utf-8"})


ast = parse.parse(js_code)
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
    StringLiteral(path) {
        path.node.extra.raw = path.node.rawValue;

    }
}


// traverse(ast,vistor1)
//
let {code} = generator(ast)

fs.writeFile('decode.js', code, (err) => {
})




