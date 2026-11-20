
# --------------------------------------------------
# SSM EC2 Security Group
# --------------------------------------------------

resource "aws_security_group" "ssm_ec2" {
  name        = "dvd-rental-${var.environment}-ssm-ec2-sg"
  description = "Security group for SSM managed EC2"
  vpc_id      = aws_vpc.main.id

  # No inbound rules required.
  # Session Manager establishes outbound connections.

  tags = {
    Name = "dvd-rental-${var.environment}-ssm-ec2-sg"
  }
}

resource "aws_vpc_security_group_egress_rule" "ssm_https" {
  security_group_id = aws_security_group.ssm_ec2.id
  description       = "Outbound HTTPS for Systems Manager"
  ip_protocol       = "tcp"
  from_port         = 443
  to_port           = 443
  cidr_ipv4         = "0.0.0.0/0"
}

resource "aws_vpc_security_group_egress_rule" "ssm_postgres" {
  security_group_id            = aws_security_group.ssm_ec2.id
  description                  = "PostgreSQL access to RDS"
  ip_protocol                  = "tcp"
  from_port                    = 5432
  to_port                      = 5432
  referenced_security_group_id = aws_security_group.rds.id
}

# --------------------------------------------------
# RDS Security Group
# --------------------------------------------------

resource "aws_security_group" "rds" {
  name        = "dvd-rental-${var.environment}-rds-sg"
  description = "Private PostgreSQL access"
  vpc_id      = aws_vpc.main.id

  tags = {
    Name = "dvd-rental-${var.environment}-rds-sg"
  }
}

resource "aws_vpc_security_group_ingress_rule" "rds_from_ssm" {
  security_group_id            = aws_security_group.rds.id
  description                  = "Allow PostgreSQL from SSM EC2 only"
  ip_protocol                  = "tcp"
  from_port                    = 5432
  to_port                      = 5432
  referenced_security_group_id = aws_security_group.ssm_ec2.id
}
