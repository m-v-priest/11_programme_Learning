

## realm表格的默认存储路径, 用Realm.defaultPath 属性就可以拿到

如果你的realm表出错, 可以将这个路径中的文件删掉,重新运行程序, 就会创建新的表.
```javascript
import Realm from 'realm'

console.log(Realm.defaultPath); //E:\phpStorm_proj\test_nodejs\default.realm
```
<br/> 

## 1.创建表, 2.向表中添加每行数据 (表.create('表头', 每项数据)), 3. 并查看表中的所有数据
```JavaScript
import Realm from 'realm'

//我们之后要添加到表中的全部数据, 暂时先放在这儿
let arrObjPerson = [
    {name: '曹操', GenerationX: 50, birthPlace: '沛国'},
    {name: '夏侯敦', GenerationX: 50, birthPlace: '沛国'},
    {name: '郭嘉', GenerationX: 70, birthPlace: '颍川'},
    {name: '刘备', GenerationX: 60, birthPlace: '幽州'},
    {name: '诸葛亮', GenerationX: 80, birthPlace: '徐州'},
    {name: '关羽', GenerationX: 60, birthPlace: '司州'},
    {name: '马超', GenerationX: 70, birthPlace: '司州'},
    {name: '姜维', GenerationX: 100, birthPlace: '凉州'},
    {name: '孙权', GenerationX: 80, birthPlace: '扬州'},
    {name: '袁绍', GenerationX: 50, birthPlace: '汝南'},
    {name: '刘表', GenerationX: 40, birthPlace: '山阳'},
    {name: '董卓', GenerationX: 30, birthPlace: '陇西'}
]


//第1步: 用一个对象, 来定义表头
let SchemaPerson = {
    name: 'SchemaPerson', //表名
    primaryKey: 'name', // 用properties对象中的用户名name, 作为主键
    // primaryKey: 主键，设置属性中的某个参数为主键。只能设置为int或者string类型.
    // 某属性设置为主键后, 它就具有唯一性, 相同值不能重复添加.

    properties: {
        id: 'int',
        name: {type: 'string', indexed: true}, //`indexed`: 索引属性，对属性进行索引将极大地加快查询的性能，但会影响插入速度。支持`string`，`int`，`bool`，`date`类型。
        GenerationX: 'int', //几零后, 比如155年诞生的, 就是50后
        birthPlace: 'string'
    }
}

// 定义一个表的配置项, 包含两个必备属性:
// (1)schema属性,用来定义我们将要创建或打开的表,其表头名是哪个.
// (2)path属性, 能指定你创建或打开的这个数据表的名字和保存路径.
let configRealm = {
    schema: [SchemaPerson],
    path: 'E:/phpStorm_proj/test_nodejs/realmSanGuo.realm' //表的保存路径
}

let idValue = 0 //定义一个初始id值, 在下面, 向表中每添加一条数据,此id值就递增1


Realm.open(configRealm)
    .then(realmCollection => {
        realmCollection.write(() => { //所有增删改查,都要在realmCollection.write()方法里来完成.

            //给表添加数据
            arrObjPerson.forEach(item => {
                let newItem = {...item, id: idValue}
                realmCollection.create('SchemaPerson', newItem) //将数组arrObjPerson中的每一项, 作为表中的每一行数据, 添加到表realmCollection中.
                idValue += 1
            })

            //----------------------------------------

            // 查看表中的所有数据
            let arrCollection = realmCollection.objects('SchemaPerson')
            console.log(arrCollection);
            console.log(arrCollection.length); //12
        })
    })
```

可以看到, 添加成功, 共12条数据  

<img src='.realm 数据库images_js/68653d4b.png' width=600></img>

<br/>

官方文档推荐把添加数据的操作, 放在try...catch语句块里面.  
Note that **any exceptions thrown in write() will cancel the transaction**. The try/catch block won’t be shown in all examples, but it’s good practice.
```javascript
try {
  realm.write(() => {
    realm.create('Car', {make: 'Honda', model: 'Accord', drive: 'awd'}); //添加每行数据
  });
} catch (e) {
  console.log("Error on creation");
}
```

<br/>

## 更新数据
官方文档的例子是这样的, 更新依然在write()方法里进行. car其实是个doc对象, 看到, 可以直接对doc对象进行属性访问.
```javascript
realm.write(() => {
  car.miles = 1100;
});
```

但是, 我的试验, 在typescript中, 对RealmObject对象的doc无法直接进行属性访问, 不知为何? 那么如何能更新doc的属性值呢?
```typescript
Realm.open(configRealm)
    .then(realmCollection => {
        realmCollection.write(() => { //所有增删改查,都要在realmCollection.write()方法里来完成.
          
            let doc曹操 = realmCollection
                .objects('SchemaPerson')
                .filtered('name = "曹操"')[0]
            console.log(doc曹操); //RealmObject { [id]: 0, [name]: '曹操', [GenerationX]: 50, [birthPlace]: '沛国' }
            // doc曹操.name //拿不到! 也就无法重新赋值
        })
    })
```

<br/>
但我们还有一种方法能够更改已存在的doc的属性值, 就是**用"主键"来帮助我们更新已存在的doc.** 依然使用create()方法, 并且第三个update参数必须是true.

表.create(type参数, properties参数, update参数)  

```typescript
Realm.open(configRealm)
    .then(realmCollection => {
        realmCollection.write(() => { //所有增删改查,都要在realmCollection.write()方法里来完成.

            let doc曹操 = realmCollection
                .objects('SchemaPerson')
                .filtered('name = "曹操"')[0]
            console.log(doc曹操); //RealmObject { [id]: 0, [name]: '曹操', [GenerationX]: 50, [birthPlace]: '沛国' }
            
            //用主键, 来给已存在的doc重新赋值属性值. 本例中,我们的主键是定义在name字段身上的.
            // 比如,如果我们想把曹操改成是90后, 那么就是如下操作, 注意, 第三个参数(update参数)必须是true!:
            realmCollection.create('SchemaPerson', {'name': '曹操', GenerationX: 90}, true) //将name是"曹操"的这条doc的GenerationX属性, 改成值是90
            // 注意, 本例中,name是主键, 在用主键来指明更新doc时, 主键必须写上, 
            //注意, create()方法中的第三个参数必须是true, 该方法的功能才是更新已有doc数据,而不是创新创建一条新的doc数据!! 这一点要牢记.
            
            console.log(doc曹操); //RealmObject { [id]: 0, [name]: '曹操', [GenerationX]: 90, [birthPlace]: '沛国' }
        })
    })
```


Creating and Updating Objects With Primary Keys  
If your model class includes a primary key, you can have Realm **intelligently update or add objects** based off of their primary key values. This is done by **passing true** as the third argument to the create method:

<br/>

## 按条件来查询数据
步骤: 
1. 用 `表.objects()方法`, 先拿到表中的所有数据,  
2. 用 `所有数据.filtered()方法`, 进行条件筛选, 
3. **注意! 筛选后所返回的是一个数组!! 哪怕你只筛选出一条结果, 也是数组!**

```javascript
Realm.open(configRealm) //把配置项传给open()方法
    .then(realmCollection => {
        realmCollection.write(() => { //所有增删改查,都要在realmCollection.write()方法里来完成.


            //要按条件查询, 必须建立在拿到表中全部数据的基础上来操作
            let arr表中所有doc = realmCollection.objects(strSchemaName) //拿到表中全部数据, 注意, 每条数据,会被realm自动封装成RealmObject对象, 而不是普通的js对象.
            console.log(arr表中所有doc);

            //----------------------------------------

            //搜索所有50后(50年代出生)的人
            let arrDoc_50后 = arr表中所有doc.filtered('GenerationX=50')
            console.log(arrDoc_50后); //[曹操, 夏侯惇, 袁绍]

            //----------------------------------------

            //搜索所有70年代后出生的, 并且籍贯是扬州的人
            let arrDoc_扬州70后及之后 = arr表中所有doc.filtered('GenerationX>=70 && birthPlace="扬州"')
            console.log(arrDoc_扬州70后及之后); //[孙权]

            //----------------------------------------

            //搜索所有姓刘的人
            let arrDoc姓刘 = arr表中所有doc.filtered('name BEGINSWITH "刘"')
            console.log(arrDoc姓刘); // [刘备, 刘表]

            //----------------------------------------

            //还支持链式过滤! 比如, 找到所有80后之后年代的人, 再找籍贯凉州的
            let arrDoc_凉州80后 = arr表中所有doc
                .filtered('GenerationX>=80')
                .filtered('birthPlace="凉州"')
            console.log(arrDoc_凉州80后); //[姜维]

            //----------------------------------------

            //找到表中最后一条数据的name属性值
            let realmObj_LastDoc = arr表中所有doc[arr表中所有doc.length - 1] //拿到的是一个RealmObject
            let objLastDoc = JSON.parse(JSON.stringify(realmObj_LastDoc)) //可以用两个JSON()方法,来把RealmObject对象转换成普通的js对象.
            console.log(objLastDoc.name); //董卓
        })
    })
```

<br/>

|                                                       |                                                              | 举例                                                         |
| ----------------------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| 数值比较运算符<br />用于类型 int, float, double, Date | = 或== <br /><=, < <br />>=, > <br />!= 或 <>                | age = 45                                                     |
| 升序或降序排列                                        | ASC, ASCENDING, <br />DESC, DESCENDING                       | age > 20 SORT(name ASC, age DESC) DISTINCT(name)             |
| 布尔比较运算符<br />用于类型 bool                     | = 或== <br/>!= 或 <>                                         |                                                              |
| 字符串类型string 支持                                 | = 或 ==<br/>!= 或 <><br/>BEGINSWITH <br/>CONTAINS  <br/>ENDSWITH | name CONTAINS 'Ja'                                           |
| 字符串还支持通配符查询                                |                                                              | name LIKE '*an?' <br />to match “Jane”, “Dan”, “Shane”, etc. |
| 使用 [c] 对字符串进行不区分大小写的比较               |                                                              | CONTAINS[c] 'Ja'                                             |
| 字符串或二进制的字符数量                              | @count 或@size                                               | name.@size = 5<br />to find all with a name of 5 letters     |
| 查询数据, 还能使用复合运算符                          | AND 或&& <br/>OR 或 \|\|                                     | name BEGINSWITH 'J' AND age >= 32                            |
| 列表支持的操作                                        | @count 或@size <br/>@min <br />@max, @sum <br/>@avg          | employees.@count > 5 <br />查找有5个元素以上的employees列表  |

<br/>

## 排序
**步骤是: 1. 找到表中所有数据, 2.用sorted()方法来排序**

即方法是:  ```表中所有数据.sorted('字段名', false或true)```

第二个参数, 默认是false, 即升序排, 从小到大排;  
如果是true, 则为倒序排, 从大到小排


```typescript
//所有增删改查,都要在realmCollection.write()方法里来完成.
Realm.open(configRealm)
    .then(realmCollection => {
        realmCollection.write(() => {


            //1. 按出生年代排序, 默认是递增(相当于第二个参数是false), 即从小到大排序. 步骤是, (1).先找到全部数据, (2).再来排序
            let arr表中所有doc = realmCollection.objects(strSchemaName)
            let arr年龄正序排 = arr表中所有doc.sorted('GenerationX') //返回的是一个数组, 里面每个元素(doc)是RealmObject对象类型
            console.log(arr年龄正序排);
            
            //----------------------------------------            
            
            //2. 想要倒序排, 即从大到小排, 只要在被排序的属性后,加上第二个参数true即可.
            let arr年龄倒序排 = arr表中所有doc.sorted('GenerationX', true) //<--注意, 第二个参数用true!
            console.log(arr年龄倒序排);
            
            //----------------------------------------            
            
            //3. 还可以用多个属性来排序. 注意, 要用一个数组来包裹住它们. 比如, 生成年代从小到大排, 相同者,就再 id值从大到小排
            let arr年龄正序id倒序排 = arr表中所有doc.sorted([['GenerationX', false], ['id', true]]) //<--注意, 第二个参数用true!
            arr年龄正序id倒序排.map(item => {
                console.log(JSON.parse(JSON.stringify(item))); //item是RealmObject对象, 我们把它转成普通js类型
            })
            /*
                { id: 11, name: '董卓', GenerationX: 30, birthPlace: '陇西' }
                { id: 10, name: '刘表', GenerationX: 40, birthPlace: '山阳' }
                { id: 9, name: '袁绍', GenerationX: 50, birthPlace: '汝南' }
                { id: 1, name: '夏侯?', GenerationX: 50, birthPlace: '沛国' }
                { id: 0, name: '曹操', GenerationX: 50, birthPlace: '沛国' }
                { id: 5, name: '关羽', GenerationX: 60, birthPlace: '司州' }
                { id: 3, name: '刘备', GenerationX: 60, birthPlace: '幽州' }
                { id: 6, name: '马超', GenerationX: 70, birthPlace: '司州' }
                { id: 2, name: '郭嘉', GenerationX: 70, birthPlace: '颍川' }
                { id: 8, name: '孙权', GenerationX: 80, birthPlace: '扬州' }
                { id: 4, name: '诸葛?', GenerationX: 80, birthPlace: '徐州' }
                { id: 7, name: '姜维', GenerationX: 100, birthPlace: '凉州' }
             */
        })
    })
```

<br/>

## 切片, 读取指定数量的数据
**步骤: 1. 先拿到表中所有数据, 2.再用slice()方法切片**
```typescript
Realm.open(configRealm) //把配置项传给open()方法
    .then(realmCollection => {
        realmCollection.write(() => {

            let arr表中所有doc = realmCollection.objects(strSchemaName)
            let arrDoc3_5 = arr表中所有doc.slice(3, 6) //包头不包尾, 拿到[3-5]的切片
            console.log(arrDoc3_5);
            /*
            [ RealmObject { [id]: 3, [name]: '刘备', [GenerationX]: 60, [birthPlace]: '幽州' },
              RealmObject { [id]: 4, [name]: '诸葛?', [GenerationX]: 80, [birthPlace]: '徐州' },
              RealmObject { [id]: 5, [name]: '关羽', [GenerationX]: 60, [birthPlace]: '司州' } ]
             */
        })
    })
```

<br/>

## 删除表中的某条数据
**步骤:   
1.先找到表中所有数据, <-- `表.objects()`  
2.再过滤出你要删除的数据, <-- `所有数据.filtered()`  
3.再删除它们 <-- `表.delete(要删除的数据)`**

比如, 我们来删除掉所有姓刘的人:
```typescript
Realm.open(configRealm) //把配置项传给open()方法
    .then(realmCollection => {
        realmCollection.write(() => { //所有增删改查,都要在realmCollection.write()方法里来完成.

            //第1步, 找到表中所有数据
            let arr表中所有doc = realmCollection.objects(strSchemaName)

            //第2步,过滤出你要删除的数据
            let arrDoc所有刘姓 = arr表中所有doc.filtered('name BEGINSWITH "刘"')

            //第3步, 删除掉你第2步过滤出的数据
            realmCollection.delete(arrDoc所有刘姓)
            console.log(arr表中所有doc); //可以看到, 刘姓已经不存在
        })
    })
```
<br/>

## 清空表
步骤: 1.先找到表中的所有数据, 2.再删除它们
```typescript
Realm.open(configRealm) //把配置项传给open()方法
    .then(realmCollection => {
        realmCollection.write(() => { //所有增删改查,都要在realmCollection.write()方法里来完成.

            //第1步: 找到表中所有数据
            let arrAllDoc = realmCollection.objects('SchemaPerson')

            //第2步: 把第1步找到的所有数据删除
            realmCollection.delete(arrAllDoc)

            console.log(arrAllDoc.length); //0 <--表已清空, 0条数据
        })
    })
```