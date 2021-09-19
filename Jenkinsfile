pipeline { 
    agent any 
    
    stages {
        stage('Get Latest Code') { 
            steps { 
                checkout scm 
            }
        }
        stage('Install Application Dependencies'){
            steps {
                echo 'Installing Dependencies....'
                sh 'source sc-env/bin/activate'
                sh 'pip3 install -r requirements.txt'
                sh 'python3 manage.py migrate'
                sh 'python3 manage.py makemigrations' 
            }
        }
    }
}