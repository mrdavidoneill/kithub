import groovy.text.SimpleTemplateEngine

pipeline {
    agent any

    environment {
        DEVELOPMENT = true
        SECRET_KEY = credentials('SECRET_KEY')
        ALLOWED_HOSTS = credentials('ALLOWED_HOSTS')
        DB_ENGINE = 'django.db.backends.mysql'
        DB_HOST = 'db'
        DB_PORT = 3306
        DB_DATABASE = 'kithub'
        DB_USER = credentials('DB_USER')
        DB_PASSWORD = credentials('DB_PASSWORD')
        MARIADB_ROOT_PASSWORD = credentials('MARIADB_ROOT_PASSWORD')
        MARIADB_DATABASE = 'kithub'
        MARIADB_USER = credentials('MARIADB_USER')
        MARIADB_PASSWORD = credentials('MARIADB_PASSWORD')
        NGINX_HOST = 'localhost'
        registry = '192.168.2.65:5000/kithub'
        dockerImage = ''
        tag = '1.0.0'
    }
    stages {
        stage('Setup .env') {
            steps {
                sh 'env > .env'
            }
        }
        stage('Build API docker image') {
            steps {
                script {
                    dockerImage = docker.build registry + '-api:test'
                }
            }
        }
        stage('Unit test') {
            steps {
                sh '''
                    docker-compose -f docker-compose-unittest.yml up --abort-on-container-exit

                    '''
            }
        }
        stage('System test') {
            steps {
                sh '''
                    docker-compose -f docker-compose-systemtest.yml up --abort-on-container-exit

                    '''
            }
        }
        stage('Acceptance test') {
            steps {
                sh '''
                    docker-compose -f docker-compose-acceptancetest.yml up --abort-on-container-exit

                    '''
            }
        }
        stage('Deploy Image') {
            steps {
                script {
                    docker.withRegistry( 'http://192.168.2.65:5000' ) {
                        dockerImage.push(tag)
                        dockerImage.push('latest')
                    }
                }
            }
        }
    }
}
