import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

// Доля ошибок
export let errorRate = new Rate('errors');

// Настройка сценария нагрузки
export let options = {
    stages: [
        { duration: '1m', target: 50 },  // рост до 50 VUs
        { duration: '1m', target: 50 },  // удержание 50 VUs
        { duration: '30s', target: 0 },  // спад до 0 VUs
    ],
    thresholds: {
        errors: ['rate<0.01'],
        'http_req_duration{name:GET /posts}': ['p(95)<500'],
        'http_req_duration{name:POST /posts}': ['p(95)<2000'],
    },
};

export default function () {
    let rand = Math.random();

    if (rand < 0.1) {
        let payload = JSON.stringify({
            author: `user_${Math.floor(Math.random() * 10000)}`,
            title: 'K6 test post',
            content: 'Content for stress test'
        });
        let params = { headers: { 'Content-Type': 'application/json' } };
        let res = http.post('http://127.0.0.1:5000/posts', payload, params);
        check(res, { 'POST /posts status 201': (r) => r.status === 201 }) || errorRate.add(1);
    } else {
        let res = http.get('http://127.0.0.1:5000/posts');
        check(res, { 'GET /posts status 200': (r) => r.status === 200 }) || errorRate.add(1);
    }

    sleep(1);
}
