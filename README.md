# ProyectoBDII_2

##  Frontend
Se elaboró un motor de búsqueda en el se visualiza un buscador y una tabla de resultados JSON, que representa los tweets.

### Integración con NodeJS y Angular

* server.js

El server recibe un archivo y lo envia al index.html para hacer mostrar una lista de tweets JSON. En caso se ingrese una palabra simple o compuesta al buscador, este hará un POST y le mandará la palabra ingresada al archivo Python para realizar la lógica de la búsqueda.

```
var bodyParser = require('body-parser');
var urlencodedParser = bodyParser.urlencoded({extended: false});

app.use(express.static(path.join(__dirname, 'dist/ang-node')));

app.use('/routes', routes);

app.get('/posts', (req, res)=>{
    res.sendFile(path.join(__dirname, 'dist/ang-node/index.html'))
})

app.get('/send', (req, res)=>{
    res.sendFile(path.join(__dirname, 'dist/ang-node/index.html'))
    //const obj = JSON.parse(JSON.stringify(req.body));
    /*const obj = JSON.parse(JSON.stringify(req.body));
    //console.log(obj.word);
    const childPython = spawn('python', ['./pythonCode/inverted_index.py', obj.word])

    childPython.stdout.on('data', (data) => {
        console.log(`${data}`);
    });
    
    childPython.stderr.on('data', (data) => {
        console.log(`stderr: ${data}`);
    });
    
    childPython.on('close', (code) => {
        console.log(`child process exited with code ${code}`);
    });*/

});

const port = process.env.PORT || 4600;

app.listen(port, (req, res)=>{
    console.log(`RUNNING on port ${port}`);
})
```

* routes.js

Recibimos el archivo JSON y lo enviamos al frontend a partir de un router tanto para la lista de JSON inicial como para el resultado de la búsqueda.

```
router.get('/posts', (req, res)=>{
    const data = JSON.parse(fs.readFileSync('./pythonCode/data/tweets_2021-06-22.json'));
    res.json(data);
})

router.get('/send', (req, res)=>{
    const newData = JSON.parse(fs.readFileSync('./pythonCode/data/result_db.json'));
    //res.json(newData);
    res.json(newData)
})
```

* posts.service.ts

Usamos un service que hará un request al server de todos los tweets y los injectará en el frontend.

```
export class PostsService {

  constructor(private http: HttpClient) { }

  getAllPosts() {
    return this.http.get('/routes/posts/').pipe(map((posts) => {
      return posts;
    }));
  }
}
```

* posts.component.ts

Cuando nuestro componente es iniciatizado, vamos a usar el método de nuestro service para recibir todos los tweets y almacenarlos en nuestro array posts.

```
export class PostsComponent implements OnInit {

  posts: any = [];

  constructor(private postService: PostsService) { }

  ngOnInit() {
    this.postService.getAllPosts().subscribe(posts => {
        this.posts = posts;
    });
  }

}
```

* send.service.ts

Usamos un service que hará un request al server de los tweet recuperados a partir del input y los injectará en el frontend.

```
export class SendService {

  constructor(private http: HttpClient) { }

  getAllPosts() {
    return this.http.get('/routes/send/').pipe(map((posts) => {
      return posts;
    }));
  }
}
```

* send.component.ts

Cuando nuestro componente es iniciatizado, vamos a usar el método de nuestro service para recibir todos los tweets y almacenarlos en nuestro array send.

```
export class SendComponent implements OnInit {

  send: any = [];

  constructor(private sendService: SendService) { }

  ngOnInit() {
    this.sendService.getAllPosts().subscribe(send => {
        this.send = send;
    });
  }

}
```


* app.module.ts

Declaramos nuestro route y lo registramos.

```
const Routes = [
  {
    path: '',
    redirectTo: 'posts',
    pathMatch: 'full'
  },
  {
    path: 'posts', component: PostsComponent
  },
  {
    path: 'send', component: SendComponent
  }
];

@NgModule({
  declarations: [
    AppComponent,
    PostsComponent,
    SendComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    RouterModule.forRoot(Routes)
  ],
  providers: [PostsService],
  bootstrap: [AppComponent]
})
export class AppModule { }
```

* posts.component.html && send.component.html

En una tabla del html, llamamos a cada elemento del JSON para que en cada fila imprima la información de un tweet.

```
<table class="table table-striped">
    <thead>
      <tr>
        <th scope="col">id</th>
        <th scope="col">date</th>
        <th scope="col">text</th>
        <th scope="col">user_id</th>
        <th scope="col">user_name</th>
        <th scope="col">location</th>
        <th scope="col">retweeted</th>
        <th scope="col">RT_text</th>
        <th scope="col">RT_user_id</th>
        <th scope="col">RT_user_name</th>
      </tr>
    </thead>
    <tbody>
      <tr *ngFor="let post of (posts OR send)">
        <td>{{post.id}}</td>
        <td>{{post.date}}</td>
        <td>{{post.text}}</td>
        <td>{{post.user_id}}</td>
        <td>{{post.user_name}}</td>
        <td>{{post.location}}</td>
        <td>{{post.retweeted}}</td>
        <td>{{post.RT_text}}</td>
        <td>{{post.RT_user_id}}</td>
        <td>{{post.RT_user_name}}</td>
      </tr>
    </tbody>
  </table>
```

## **2. BackEnd**

### **2.1 Observaciones:**
* Como estamos trabajando con varios archivos de tipo json, donde cada uno contiene varios tweets, es necesario asignar un identificador a cada archivo. Por lo que, vamos a apoyarnos de un diccionario, donde la _key_ es el identificador del archivo y el _value_ es el nombre del archivo.

* Hemos trabajado con 479 945 tweets.

* Hemos creado el índice invertido a partir 128 562 términos únicos. 

* A cada término le hemos asignado un identificador, por lo que nos apoyamos de un diccionario donde la _key_ es el término y el _value_ es el ID del término.

* Como un tweet se encuentra en un archivo de tipo json; asimismo, tiene su longitud (norma) y tiene un conjunto de términos donde cada término tiene su peso tf.idf es necesario realizar un mapeo de estos elementos de un tweet con un diccionario. En este diccionario, la _key_ es el ID del tweet y el _value_ es la lista de los elementos mencionados anteriormente. 

* Cada término aparece en diferentes tweets por lo que esta cantidad de apariciones es mapeada por un diccionario. Donde la _key_ es el ID del término y el _value_ es la frecuencia de documentos (df) 

* Por la elevada cantidad de tweets,  la creación de los diccionarios demora un tiempo considerable, alrededor de 10 minutos, por lo que estos los guardamos en archivos binarios con ayuda de la librería pickle. 


### **2.2 Creación del índice**

En primer lugar, al procesar cada tweet realizamos el parser correspondiente para obtener los términos que nos importan, es decir, eliminando los stopwords y obteniendo la raíz de cada token. Luego de procesar todos los tweets, recién es posible obtener la norma de un tweet  y el peso tf.idf de cada término respecto a ellos. Finalmente, guardamos en archivos binarios todos los diccionarios mencionados en la sección de Observaciones, la cantidad de tweets procesados y la cantidad de términos. Esto se aprecia en el jupyter-notebook del repositorio.

### **2.3 Funciones**

Realizamos una descripción de las funciones que hemos utilizado:

**stopwords_stemmer(text)**
* Dicha función recibe una cadena de caracteres, dicha cadena pasa por un proceso de tokenización en el que se coloca cada palabra en una lista. Luego, se aplica la función stopwords que retirará las palabras más comunes que no aportan un significado a la búsqueda. Después, aplicamos la función stemmer a cada palabra para obtener la raíz de dicha palabra. Finalmente, retornamos la lista de palabras totalmente filtradas y reducidas a su raíz.

**searchKNN(query, k)**
* Recibe como parámetro la consulta del usuario y la cantidad de tweets que serán mostrados en el Frontend. Esta función retorna una lista de K tuplas que contiene el id del tweet y la distancia que representa la similitud entre la consulta del usuario y el texto del tweet. 

**retrieve_tweets(query, k)**
* Para la recuperación de los datos se hace uso de un vector que contiene el id de los K tweets con mayor similitud con respecto a la consulta del usuario. Dicho vector se obtuvo a través de la función _searchKNN()_. Cada id que contiene el vector es pasado a la función retrieve_tweet el cual recibe un id_tweet y retorna toda la información tweet en formato json. Finalmente, retornaremos el arreglo de Json que compone cada tweet que será mostrado en el Frontend.

**retrieve_tweet(docID)**
* Dicha función recibe un id del tweet a buscar, retornando la información respecto al tweet una vez encontrado en el json.

## **3. Pruebas de rendimiento**
### **3.1 Experimento**
A partir de una consulta, realizamos la búsqueda de los _K_ tweets con mayor similitud con respecto a ella. Donde el valor de _K_ se encuentra variando.

* Consulta N°1 = _"Los congresistas fujimoristas son delincuentes"_
* Consulta N°2 = _"Necesitamos autoridades honestas"_
* Consulta N°3 = _"Daniel Urresti lidera las encuestas"_
  
| Consulta \ k | K = 1 | K = 5 | K = 20 | K = 100 | k = 1000 |
|--------------|-------|-------|--------|---------|----------|
| Consulta N°1 |       |       |        |         |          |
| Consulta N°2 |       |       |        |         |          |
| Consulta N°3 |       |       |        |         |          |

### **3.2 Conclusiones**
* La búsqueda de los _K_ tweets con mayor similitud es eficiente puesto que no demora mas de x segundos para encontrarlos, a pesar de tener buscar entre 480 mil tweets
* Asimismo, el tamaño de la consulta no afecta al rendimiento de la búsqueda.