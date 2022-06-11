


## Promise的状态
Promise对象是一个容器, 里面保存着一个异步操作(即某个非立即完成的, 而是未来才会做完的事件). 那么这个异步操作就有三种可能的状态: pending（进行中）、fulfilled（已成功）和rejected（已失败）。使得Promise对象也有这三种状态.

无论从pending变为fulfilled, 还是从pending变为rejected, 都叫做resolved（已定型）。

<br/>  

## Promise的特点(优缺点)是:  
* 一旦新建Promise对象, 它就会立即执行，无法中途取消执行。
* Promise内部抛出的错误，不会反应到外部, 除非你设置回调函数。
* 当处于pending状态时，无法得知目前进展到了哪一个阶段（刚刚开始还是即将完成）。

<br/>

## 新建一个promise实例
比如, 读取一个文章, fs是异步操作.
```javascript
let fs = require('fs')

//自定义一个函数, 用来封装promise对读取文件的操作, 并返回一个promise对象
function fnPms_readFile(urlFile) {
    //Promise构造函数接受一个函数作为参数，该函数的两个参数分别是resolve和reject,它们是两个函数。
    let pms = new Promise((res, rej) => {
        fs.readFile(urlFile, (err, data) => {
            if (err) {
                rej(err) //用rej函数来处理异步操作的出错时的结果. 
            }
            else {
                res(data) //用res函数来处理异步操作的成功结果. 
            }
        })
    })
    return pms
}

let urlFile = './poemWangChuYi.txt' 

fnPms_readFile(urlFile)
    .then(data => { //上面res接收的参数,会传给这里then方法的回调函数中
        console.log(data.toString()); //data即古诗内容,别忘了需用toString()来转成字符串
    })
    .catch(err => { //上面rej接收的参数,会传给这里catch方法的回调函数中
        console.log(err);
    })
```

<br/>  

## res()函数, 除了可以接收一个普通的数据类型外, 还可以接收一个promise对象.   
这样,then()方法就能接收到这个pms对象.  
**then()方法也返回的是一个新的Promise实例**（注意，不是它接收的那个Promise实例）。因此可以采用链式写法，即then方法后面再调用另一个then方法。


<br/>  

## Promise 新建后就会立即执行  
```javascript
let pms = new Promise((res, rej) => {
    console.log('111'); //Promise 新建后就会立即执行.
    return res() //一般来说，调用resolve或reject以后，Promise 的使命就完成了，后继操作应该放到then方法里面，而不应该直接写在resolve或reject的后面。所以，最好在它们前面加上return语句，这样就不会有意外。
})

pms.then(data => {
    console.log('222');
})

console.log('333');

/* 执行顺序为:
111
333
222
 */
```

<br/>  

## Promise.all() 
Promise.all方法接受一个数组作为参数，数组中的每项(比如叫p1、p2、p3), 都是一个promise对象.  
p1、p2、p3的返回值, 会组成一个数组, 传递给Promise.all() .then()方法的参数中.  
**注意: 返回值的排序与你数组中各个promise对象排序顺序完全一致。**

```javascript
let fs = require('fs')

//自定义一个函数, 用来封装promise对读取文件的操作, 并返回一个promise对象
function fnPms_readFile(urlFile) {
    let pms = new Promise((res, rej) => {
        fs.readFile(urlFile, (err, data) => {
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

let p1 = fnPms_readFile(urlFile1)
let p2 = fnPms_readFile(urlFile2)
let p3 = fnPms_readFile(urlFile3)

//Promise.all方法用于将多个 Promise 实例，包装成一个新的 Promise 实例, 并返回它。
Promise.all([p1, p2, p3])
    .then(arrData => {
        console.log(Array.isArray(arrData)); //true <--Array.isArray() 用来判断一个变量是否是数组类型
        console.log(arrData); //打印出一个数组, 每一项,就是一个poem.txt文件的内容.

        arrData.forEach(item => {
            console.log(item.toString());
        })
    })

```

<br/>  

## Promise.race()  
Promise.race()方法同样是将多个 Promise 实例，包装成一个新的 Promise 实例返回。  
race就是赛跑的意思，意思就是说，Promise.race([p1, p2, p3])里面哪个结果获得的快，就返回那个结果，不管结果本身是成功状态还是失败状态。

```javascript
Promise.race([p1, p2, p3])
    .then(firstData => {
        console.log(firstData);
    })
```

<br/>

## Promise.resolve() 能将一个普通数据类型, 转成promise对象. 相当于封装了一下.

```javascript
let strName = 'objZzr'

Promise.resolve(strName) //将字符串封装成promise对象
    .then(data => {
        console.log(data); //zzr
    })

//上面的写法等价于
new Promise((res, rej) => {
    res(strName)
}).then(data => {
    console.log(data); //zzr
})
```






















































