

## 用返回this, 来实现链式方法调用
```typescript
class Cls计算器 {
    protected numValue: number

    constructor(numValue: number) {
        this.numValue = numValue;
    }

    fnAdd(num2: number): this { //加法
        this.numValue += num2
        return this //返回this, 使得本类的实例能够链式调用实例方法
    }

    fnMultiply(num2: number): this { //乘法
        this.numValue *= num2
        return this //返回this, 使得本类的实例能够链式调用实例方法
    }

    fnGetCurrentValue(): number {
        return this.numValue
    }
}

//链式调用
let numValue = new Cls计算器(5)
    .fnAdd(2)
    .fnMultiply(3)
    .fnGetCurrentValue()
console.log(numValue); //21 <== 即(5+2)*3


//子类继承父类
class Cls高级计算器 extends Cls计算器 {

    constructor(numValue: number) {
        super(numValue);
    }

    fnPow(numPowerful: number): this { //指数
        this.numValue = Math.pow(this.numValue, numPowerful) //pow() 方法可返回 x 的 y 次幂的值。
        return this
    }
}

let numValue2 = new Cls高级计算器(3)
    .fnAdd(2)
    .fnPow(3)
    .fnMultiply(4)
    .fnGetCurrentValue()
console.log(numValue2); //500 <== 即 ((3+2)^3)*4
```