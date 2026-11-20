
# --------------------------------------------------
# Amazon Linux 2023 AMI
# --------------------------------------------------

data "aws_ssm_parameter" "al2023_ami" {
  name = "/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64"
}

# --------------------------------------------------
# EC2 IAM Role
# --------------------------------------------------

data "aws_iam_policy_document" "ssm_assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "ssm_ec2" {
  name               = "dvd-rental-${var.environment}-ssm-ec2-role"
  assume_role_policy = data.aws_iam_policy_document.ssm_assume_role.json
}

resource "aws_iam_role_policy_attachment" "ssm_core" {
  role       = aws_iam_role.ssm_ec2.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

resource "aws_iam_instance_profile" "ssm_ec2" {
  name = "dvd-rental-${var.environment}-ssm-ec2-profile"
  role = aws_iam_role.ssm_ec2.name
}

# --------------------------------------------------
# SSM EC2 Instance
# --------------------------------------------------

resource "aws_instance" "ssm" {
  ami                         = data.aws_ssm_parameter.al2023_ami.value
  instance_type               = var.ssm_instance_type
  subnet_id                   = aws_subnet.public.id
  vpc_security_group_ids      = [aws_security_group.ssm_ec2.id]
  associate_public_ip_address = true
  iam_instance_profile        = aws_iam_instance_profile.ssm_ec2.name

  metadata_options {
    http_endpoint = "enabled"
    http_tokens   = "required"
  }

  root_block_device {
    volume_size           = 8
    volume_type           = "gp3"
    encrypted             = true
    delete_on_termination = true
  }

  tags = {
    Name = "dvd-rental-${var.environment}-ssm-instance"
  }

  depends_on = [
    aws_iam_role_policy_attachment.ssm_core
  ]
}
