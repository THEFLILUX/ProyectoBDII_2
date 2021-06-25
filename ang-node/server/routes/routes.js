const fs = require('fs');
const express = require('express');
const router = express.Router();
const axios = require('axios');

const PostAPI = 'https://jsonplaceholder.typicode.com';


router.get('/', (req, res)=>{
    res.send('it works');
})

router.get('/posts', (req, res)=>{
    const data = JSON.parse(fs.readFileSync('./pythonCode/data/tweets_2021-06-22.json'));
    res.json(data);
})

module.exports = router;