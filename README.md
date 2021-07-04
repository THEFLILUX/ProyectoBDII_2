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
