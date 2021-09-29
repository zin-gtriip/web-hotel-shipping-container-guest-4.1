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

                git credentialsId: 'phuwai-bitbucket', url: 'https://source.gtriip.com/scm/web_app/shippingcontainer_guest.git'
                sh 'ls'

                sshagent (credentials: ['ssh-jenkinstest']) {
                    sh 'pwd'
                    sh '''
                        ssh -tt -o StrictHostKeyChecking=no phu@18.141.54.154 "cd shippingcontainer_guest &&
                        ls &&
                        pwd &&
                        git pull &&  
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