pipeline { 
    agent any 
    
    stages {
        stage('Get Latest Code') { 
            steps { 
                checkout scm 
            }
        }
        stage('Deploy'){
            environment {
                GIT_CREDS = credentials('phuwai-bitbucket')
            }
            steps {
                echo 'Deploying.....'

                git credentialsId: 'phuwai-bitbucket', url: 'https://source.gtriip.com/scm/web_app/shippingcontainer_guest.git'
                sh 'ls'

                sshagent (credentials: ['ssh-jenkinstest']) {
                    sh 'pwd'
                    sh '''
                        ssh -tt -o StrictHostKeyChecking=no phu@18.141.54.154 "cd shippingcontainer_guest &&
                        ls &&
                        pwd &&
                        echo 'SSH user is $GIT_CREDS_USR' &&
                        echo 'SSH user is $GIT_CREDS_PSW' &&
                        docker-compose down &&
                        docker-compose build &&
                        docker-compose image prune &&
                        docker-compose up -d"
                    '''
                }
                
            }
        }
    }
}