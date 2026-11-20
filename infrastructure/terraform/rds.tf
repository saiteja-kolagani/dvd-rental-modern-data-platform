
# --------------------------------------------------
# RDS DB Subnet Group
# --------------------------------------------------

resource "aws_db_subnet_group" "main" {
  name = "dvd-rental-${var.environment}-db-subnet-group"

  subnet_ids = [
    aws_subnet.private_a.id,
    aws_subnet.private_b.id
  ]

  tags = {
    Name = "dvd-rental-${var.environment}-db-subnet-group"
  }
}

# --------------------------------------------------
# RDS PostgreSQL
# --------------------------------------------------

resource "aws_db_instance" "postgres" {
  identifier = var.db_identifier

  engine         = "postgres"
  engine_version = var.db_engine_version
  instance_class = var.db_instance_class

  db_name  = var.db_name
  username = var.db_username

  manage_master_user_password = true

  allocated_storage = var.db_allocated_storage
  storage_type      = "gp3"
  storage_encrypted = true


  availability_zone   = "ap-south-1b"
  multi_az            = false
  publicly_accessible = false

  port                   = 5432
  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.rds.id]

  backup_retention_period = 1
  copy_tags_to_snapshot   = true

  deletion_protection       = true
  skip_final_snapshot       = false
  final_snapshot_identifier = "dvd-rental-${var.environment}-final-snapshot"

  auto_minor_version_upgrade = true
  apply_immediately          = false

  tags = {
    Name = "dvd-rental-${var.environment}-postgres"
  }

  lifecycle {
    prevent_destroy = true
  }
}
