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
    }
    stages {
        stage('Build API docker image') {
            steps {
                sh 'env > .env'
                script {
                    dockerImage = docker.build registry + '-api:test'
                }
            }
        }
        stage('Test') {
            parallel {
                stage('Unit test') {
                    environment {
                        DB_HOST = 'db_unittest'
                    }
                    steps {
                        sh 'env > .env'
                        sh '''
                            docker-compose -f docker-compose-unittest.yml up --abort-on-container-exit

                            '''
                    }
                }
                stage('System test') {
                    environment {
                        DB_HOST = 'db_systemtest'
                    }
                    steps {
                        sh 'env > .env'
                        sh '''
                            docker-compose -f docker-compose-systemtest.yml up --abort-on-container-exit

                            '''
                    }
                }
            }
        }
    }
}
