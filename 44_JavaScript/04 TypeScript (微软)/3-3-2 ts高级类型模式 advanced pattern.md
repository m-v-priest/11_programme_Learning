
## 对一个联合类型(or或的关系), 进行类型辨识
你可以合并单例类型，联合类型，类型保护和类型别名, 来创建一个叫做 "可辨识联合（Discriminated Unions）"的高级类型模式，它也称做 "标签联合"或"代数数据类型"。  
 You can combine `singleton types`, `union types`, `type guards`, and `type aliases` to build an `advanced pattern` called `discriminated unions`, also known as `tagged unions` or `algebraic data types`. 
 
 ```typescript
 interface Square {
    kind: "square"; //每个接口都有 kind属性, 但有不同的字符串字面量的类型。kind属性称做 "可辨识的特征(discriminant)"或"标签(tag)"。
    size: number; //其它的属性则为各个接口独有。
}

interface Rectangle {
    kind: "rectangle";
    width: number;
    height: number;
}

interface Circle {
    kind: "circle";
    radius: number;
}

type Shape = Square | Rectangle | Circle; //我们把上面的各个接口联合到一起

function area(s: Shape) { //Shape类型就是上面所有接口的联合类型(或or的关系).
    switch (s.kind) { //用kind属性来进行不同接口的辨识
        case "square":
            return s.size * s.size;
        case "rectangle":
            return s.height * s.width;
        case "circle":
            return Math.PI * s.radius ** 2;
    }
}
 ```
 
 ## 对"联合类型"的使用, 进行"完整性检查", 即, 检测是否用到了联合类型中的所有类型? 是否有哪个类型没被使用到, 遗漏了?
 
 默认情况下, 如果你对"联合类型"中的某些类型没有用得到, 代码是不会提醒你的.
 ```typescript
 interface ItfA {
    kind: 'ItfA'
    attr1: string
}

interface ItfB {
    kind: 'ItfB'
    attr2: number
}

interface ItfC {
    kind: 'ItfC'
    attr3: boolean
}

interface ItfD {
    kind: 'ItfD'
    attr4: object
}

type typeCombine = ItfA | ItfB | ItfC | ItfD

function fn(type: typeCombine) { //注意: 本函数中,我们漏写了type是ItfD的类型,但函数没有提示我们, 这是个问题...
    switch (type.kind) {
        case 'ItfA':
            return ''
        case 'ItfB':
            return ''
        case 'ItfC':
            return ''
    }
}
```
 
 那么, 如我我们想让代码提示我们有遗漏, 该怎么做呢?  
 方法就是: 使用 never类型，编译器会用它来进行完整性检查：
 ```typescript
 interface ItfA {
    kind: 'ItfA'
    attr1: string
}

interface ItfB {
    kind: 'ItfB'
    attr2: number
}

interface ItfC {
    kind: 'ItfC'
    attr3: boolean
}

interface ItfD {
    kind: 'ItfD'
    attr4: object
}

type typeCombine = ItfA | ItfB | ItfC | ItfD

function fn(type: typeCombine): never { //注意: 本函数中,我们漏写了type是ItfD的类型
    switch (type.kind) {
        case 'ItfA':
            return ''
        case 'ItfB':
            return ''
        case 'ItfC':
            return ''
    }
} dirGrandfather
// 说明, 我们让函数fn返回never类型后, 必须让这个fn函数有一个不可能达到的终点. 比如我们要让其"报错", 才能实现这一目标.
 ```
 
 下面继续来完善上面的代码
 ```typescript
 interface ItfA {
    kind: 'ItfA'
    attr1: string
}

interface ItfB {
    kind: 'ItfB'
    attr2: number
}

interface ItfC {
    kind: 'ItfC'
    attr3: boolean
}

interface ItfD {
    kind: 'ItfD'
    attr4: object
}

type typeCombine = ItfA | ItfB | ItfC | ItfD

//我们来定义一个函数, 专门用来抛出错误. 所以该函数的返回值也肯定是never类型了.
function fn_ThrowError(arg: any): never {
    throw new Error(`${JSON.stringify(arg)}此类型并未在函数中被处理,缺少处理此类型的相关代码!`)
}

function fn(itf: typeCombine) { //注意: 本函数中,我们漏写了ift是ItfD的类型
    switch (itf.kind) {
        case 'ItfA':
            return ''
        case 'ItfB':
            return ''
        case 'ItfC':
            return ''
        default: //switch中的default，一般用在最后，表示非以上的任何情况下发生的情况, 即, 不是上面这三种情况, 那就一定是剩下的一个接口ItfD了
            return fn_ThrowError(itf) //此itf参数, 会被传入的实参一定就是ItfD
    }
}

//上面, 函数都定义好了, 下面来正式做实验, 看看我们上面的fn函数, 会不会提醒我们遗漏使用了ItfD类型

let insA: ItfA = {
    attr1: "", kind: "ItfA"
}

let insD: ItfD = {
    attr4: {}, kind: "ItfD"
}

fn(insA) //ok, 没问题
fn(insD) //Error: {"attr4":{},"kind":"ItfD"}此类型并未在函数中被处理,缺少处理此类型的相关代码! <--成功提示!
 ```
 **上面这种方式需要你定义一个额外的函数(专门用来用报错的方式,给出提示信息)**，但是在你忘记某个case的时候也更加明显, 很实用。
 
 