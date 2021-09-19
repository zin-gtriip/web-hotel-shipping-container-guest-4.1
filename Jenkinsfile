pipeline { 
    agent any 
    
    stages {
        stage('Get Latest Code') { 
            steps { 
                checkout scm 
            }
        }
        stage('Deploy'){
            steps {
                echo 'Deploying.....'
                sh "chmod +x -R ${env.WORKSPACE}"
                sh "./deploy_qa.sh"
                
            }
        }
    }
}