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
                    sh 'ssh -tt -oStrictHostKeyChecking=no jenkins@54.179.10.115'
                    sh 'ssh -tt -oStrictHostKeyChecking=no jenkins@54.179.10.115 git pull'
                    sh 'ls'
                    sh 'cd ..'
                    sh 'ls -l -a'
                    sh 'cd GuestFacing/shippingconatiner_guest'
                    sh 'git pull'
                    sh 'docker-compose pull'
                    sh 'docker-compose up -d'
                }
                
            }
        }
    }
}