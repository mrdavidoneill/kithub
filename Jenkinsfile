pipeline {
    agent any
    stages {
         stage('Setup Python Virtual Environment'){
            steps {
                sh '''
                    chmod +x ./scripts/envsetup.sh
                    ./scripts/envsetup.sh
                    '''
            }
        }
        stage('Unit test'){
            steps {
                sh '''
                    chmod +x ./scripts/unittest.sh
                    ./scripts/unittest.sh
                    '''
            }
        }
    }
}