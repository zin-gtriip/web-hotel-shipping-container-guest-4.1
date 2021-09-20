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
                sshagent (credentials: ['ssh-shippingcontainer']) {
                    sh '''
                        ssh -t phu@54.179.10.115 "cd GuestFacing/shippingcontainer_guest && 
                        git pull && 
                        docker-compose pull &&
                        docker-compose up -d"
                    '''
                }
                
            }
        }
    }
}