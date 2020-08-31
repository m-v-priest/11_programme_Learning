


> async [ə'zɪŋk] adj.异步的  
> a-,不，非，synchronous,同时的。at- 去，往来自ad-在字母t 前的拼写异化形式。

<br/>

## async函数的用法


```javascript
let fs = require('fs')

//自定义一个函数, 用来封装promise对读取文件的操作, 并返回一个promise对象
function fnPms_readFile(urlFile) {
    let pms = new Promise((res, rej) => {
        fs.readFile(urlFile, 'utf-8', (err, data) => { //别忘了第二个参数加上 'utf-8', 这样, 读取到的data就是字符串了, 而不是一个二进制数据, 即 你的data就不需要再用toString()来转成字符串了!
            if (err) {
                rej(err)
            }
            else {
                res(data)
            }
        })
    })
    return pms
}

let urlFile1 = './poem1.txt'
let urlFile2 = './poem2.txt'
let urlFile3 = './poem3.txt'

//async表示这个函数里有异步操作
async function fnAsc_readFileOneByOne() {
    let str1 = await fnPms_readFile(urlFile1) //await会等待后面后面的异步操作, 拿到结果。
    //即, 如果只写fnPms_readFile()函数,会返回一个promise对象; 而在前面加了await后, 整个语句 await fnPms_readFile(), 就会返回一个该函数读取的文件中的字符串内容了! 相当于解除了promise容器的封装, 直接取到了里面的值.
    let str2 = await fnPms_readFile(urlFile2)
    let str3 = await fnPms_readFile(urlFile3)
    console.log(str1, str2, str3); //即三个文件的字符串内容
}

fnAsc_readFileOneByOne()
```
<br/>

## async函数的返回值, 依然是一个promise对象  
**async函数有返回值, 依然会返回一个 Promise 对象.**  
async函数返回的 Promise 对象，必须等到内部所有await命令后面的 Promise 对象都执行完，才会发生状态改变，除非遇到return语句或者抛出错误。也就是说，只有async函数内部的异步操作都执行完，才会执行then方法指定的回调函数。

<br/>

## await命令只能用在async函数之中   
await 如果用在普通函数，就会报错。

<br/>

## await 后面, 可以跟 Promise 对象, 也可以跟原始类型的值（数值、字符串和布尔值)
如果是跟原始数据类型的值的话, 会自动转成立即 resolved 的 Promise 对象. 即, **虽然await会把后面的值转成纯数据(比如直接拿到字符串), 但async函数会返回一个promise对象, 是不会变的.**

```javascript
async function fnAsc() {
    let str = await 'objZzr' //<--注意, 这里await后面跟的是一个基本数据类型.
    console.log(str); //zzr
    return str //async函数会返回一个promise对象, 即会把这个str封装成promise对象
}

fnAsc()
    .then(data => {
        console.log(data); //zzr
    })
    .catch(err => {
        console.log(err);
    })
```

<br/>

## 如果 await后的 promise对象变成了 reject状态, 错误会被之后的catch()的回调函数捕获到.  
await命令后面的 Promise 对象, 如果变为reject状态，则reject中参数, 就能被之后的catch方法的回调函数接收到。即使这个await前面不加return, 也没关系, 错误依然能被之后的catch()捕获到.
```javascript
async function fnAsc(){
    await Promise.reject('explode!!') //在await前面加不加return, 后面pms对象的拒绝态错误, 都能被下面的catch方法的回调函数捕获到. 当然, 你加了return, 结果也是一样的.
}

fnAsc()
    .then()
    .catch(err=>{
    console.log(err);}) //explode!!
```

<br/>

## 任何一个await语句后面的 Promise 对象变为reject状态，那么整个async函数都会中断执行。即,该await后面的其他await都不会再去执行了.

```javascript
async function fnAsc(){
    await Promise.reject('explode!!')
    return await Promise.resolve('i am zzr') //这句不会执行, 因为上面已经是rej态了

}

fnAsc()
    .then(data=>{
        console.log(data); //这里不会打印
    })
    .catch(err=>{
    console.log(err);}) //explode!!
```

**有时，我们希望即使前一个异步操作失败，也不要中断后面的异步操作。有两种方法可以实现这个目的:**  

1. 可以将第一个await放在try...catch结构里面，这样不管这个异步操作是否成功，第二个await都会执行。 

```javascript
async function fnAsc(){
    try {
        await Promise.reject('explode!!')
    }catch (e) {
        console.log(e); //注意, 如果这里 return了err, 则下面的'i am zzr'语句就不会再被return了. 即下面的语句不会被执行.
    }
    return await Promise.resolve('i am zzr') //这句依然会执行, 因为上面的rej态被装在了try...catch语句里. 
}

fnAsc()
    .then(data=>{
        console.log(data); 
    })
    .catch(err=>{
    console.log(err);}) 

/* 执行结果
explode!!
i am zzr
*/
```
2. 另一种方法是await后面的 Promise 对象再跟一个catch方法，处理前面可能出现的错误。
```javascript
async function fnAsc() {
    await Promise.reject('explode!!')
        .catch(e => { //<--直接用catch语句来处理本pms的拒绝态
            console.log(e);
        })
    return await Promise.resolve('i am zzr') //这句依然会执行
}

fnAsc()
    .then(data => {
        console.log(data);
    })
    .catch(err => {
        console.log(err);
    })

/* 执行结果
explode!!
i am zzr
*/
```

<br/>

## 多个await命令后面的异步操作，如果不存在继发关系，最好让它们同时触发。  
```javascript
//延时拿到str
function fnPms(str, milliseconds) {
    return new Promise((res, rej) => {
        setTimeout(() => {
            res(str) //n秒后再调用res函数
        }, parseInt(milliseconds))
    })
}

async function fnAsc_继发() {
    let str1 = await fnPms('objZzr', 500)
    let str2 = await fnPms('wyy', 100)
    let str3 = await fnPms('mwq', 2000)
    console.log(str1, str2, str3);
}

//Promise.all()方法, 能让多个异步操作并发执行
async function fnAsc_同时触发() {
    let arrStr = await Promise.all([fnPms('objZzr', 500), fnPms('wyy', 800), fnPms('mwq', 1000)]) //Promise.all(iterable) 方法返回一个 Promise 实例, 但是由于前面又加了await, 于是就直接把这个pms对象解封了, 拿到了里面的数组.
    console.log(arrStr);
}

fnAsc_继发() //后打印 zzr wyy mwq
fnAsc_同时触发() //先打印 [ 'zzr', 'wyy', 'mwq' ] <--同时触发，能大大缩短程序的执行时间
```

但如果一定要用继发, 如果有多个await命令，可以统一放在try...catch结构中。 **事实上, await命令后面的Promise对象，运行结果可能是rejected，所以最好把await命令放在try...catch代码块中。** 
```javascript
async function main() {
  try {
    const val1 = await firstStep();
    const val2 = await secondStep(val1);
    const val3 = await thirdStep(val1, val2);

    console.log('Final: ', val3);
  }
  catch (err) {
    console.error(err);
  }
}
```



<br/>

## async 函数有多种使用的形式
```javascript
// 函数声明
async function fnName() {}

// 函数表达式
const fnName = async function () {};

// 箭头函数, 也能设为 async的(异步的)
const fnName = async () => {};

// 可以将对象的方法, 设为 async方法 
let obj = { async fnName() {} };
obj.fnName().then()


// Class 的方法, 也能设为 async方法
class ClsName{
    constructor(){}
    
    async fnAsc(){
        let data = await objPms
        return data //async函数会返回一个pms对象,即会把这个data封装成pms对象后再return出去.
    }
}

let ins = new ClsName()
ins.fnAsc().then()
```

<br/>
   
## async箭头函数的用法  
```javascript
//延时拿到str
function fnPms(str, milliseconds) {
    return new Promise((res, rej) => {
        setTimeout(() => {
            res(str) //n秒后再调用res函数
        }, parseInt(milliseconds))
    })
}

let p1 = fnPms('objZzr', 500)
let p2 = fnPms('wyy', 1000)
let p3 = fnPms('mwq', 2000)

function fn并发执行() {
    let arrPms = [p1,p2,p3]
    arrPms.forEach(async (pms)=>{ //async箭头函数的用法
        console.log('并发',await pms);
    })
}

fn并发执行()
```
