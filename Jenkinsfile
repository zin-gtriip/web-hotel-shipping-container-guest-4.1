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
                    sh 'ssh phu@54.179.10.115'
                    sh 'whoami'
                    sh 'pwd'
                    sh '#!/bin/bash'
                    sh'pwd'
                    sh 'cd /var/jenkins_home/workspace/shippingconatiner-guestfacing@3'
                    sh 'ls'
                    sh 'git pull'
                    sh 'docker-compose pull'
                    sh 'docker-compose up -d'
                }
                
            }
        }
    }
}